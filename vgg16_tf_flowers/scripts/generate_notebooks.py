#!/usr/bin/env python3
"""Genera seis Colabs autónomos a partir del flujo de las plantillas del profesor."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NB_DIR = ROOT / "notebooks"


def source(text):
    return [line + "\n" for line in text.strip("\n").splitlines()]


def markdown(text):
    return {"cell_type": "markdown", "metadata": {}, "source": source(text)}


def code(text):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source(text),
    }


SETUP = r'''
# ADAPTADO: dependencias adicionales para TFDS, métricas y gráficas
%pip -q install --upgrade "tensorflow-datasets>=4.9,<5.0" "scikit-learn>=1.6,<2.0" seaborn==0.13.2 pydot graphviz

import hashlib, importlib.metadata, json, os, platform, random, time
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
import tensorflow_datasets as tfds
from sklearn.model_selection import train_test_split
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Model

SEMILLA = 42
TAMANIO_IMAGEN = (224, 224)
BATCH_SIZE = 16
EPOCAS = 30
CLASES = ["dandelion", "daisy", "tulips", "sunflowers", "roses"]
RAIZ = Path.cwd()
for carpeta in ["data", "weights", "results", "figures"]:
    (RAIZ / carpeta).mkdir(exist_ok=True)

os.environ["PYTHONHASHSEED"] = str(SEMILLA)
random.seed(SEMILLA)
np.random.seed(SEMILLA)
tf.keras.utils.set_random_seed(SEMILLA)
try:
    tf.config.experimental.enable_op_determinism()
except Exception:
    pass

print("TensorFlow:", tf.__version__)
print("TFDS:", importlib.metadata.version("tensorflow-datasets"))
print("Python:", platform.python_version())
print("GPU:", tf.config.list_physical_devices("GPU"))
'''

DATA = r'''
# 1. Cargar las imágenes: ADAPTADO de directorios a tf_flowers (5 clases)
dataset_base, info = tfds.load(
    "tf_flowers:3.0.1", split="train", as_supervised=True,
    with_info=True, shuffle_files=False
)
assert info.features["label"].num_classes == 5
CLASES = list(info.features["label"].names)
TOTAL = info.splits["train"].num_examples
etiquetas = np.fromiter((int(y) for _, y in tfds.as_numpy(dataset_base)), dtype=np.int64, count=TOTAL)
indices = np.arange(TOTAL, dtype=np.int64)

# Partición estratificada 70/15/15; la misma semilla produce el mismo manifiesto.
idx_train, idx_temp, y_train, y_temp = train_test_split(
    indices, etiquetas, test_size=0.30, random_state=SEMILLA, stratify=etiquetas
)
idx_val, idx_test, y_val, y_test = train_test_split(
    idx_temp, y_temp, test_size=0.50, random_state=SEMILLA, stratify=y_temp
)
asignacion = np.empty(TOTAL, dtype=object)
asignacion[idx_train], asignacion[idx_val], asignacion[idx_test] = "train", "validation", "test"
manifiesto = pd.DataFrame({"index": indices, "label": etiquetas, "split": asignacion})
ruta_manifiesto = RAIZ / "data" / "split_manifest.csv"
if ruta_manifiesto.exists():
    anterior = pd.read_csv(ruta_manifiesto)
    pd.testing.assert_frame_equal(anterior, manifiesto, check_dtype=False)
else:
    manifiesto.to_csv(ruta_manifiesto, index=False)
assert manifiesto["index"].is_unique and len(manifiesto) == TOTAL
assert set(manifiesto["split"]) == {"train", "validation", "test"}

def seleccionar(indices_split):
    llaves = tf.constant(np.asarray(indices_split), dtype=tf.int64)
    tabla = tf.lookup.StaticHashTable(
        tf.lookup.KeyValueTensorInitializer(llaves, tf.ones_like(llaves, dtype=tf.int32)),
        default_value=0,
    )
    ds = dataset_base.enumerate()
    ds = ds.filter(lambda i, elemento: tabla.lookup(i) > 0)
    return ds.map(lambda i, elemento: elemento, num_parallel_calls=tf.data.AUTOTUNE)

aumento = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal", seed=SEMILLA),
    tf.keras.layers.RandomRotation(0.08, seed=SEMILLA),
    tf.keras.layers.RandomZoom(0.10, seed=SEMILLA),
], name="aumento_solo_entrenamiento")

def preparar(ds, entrenando=False):
    ds = ds.map(
        lambda x, y: (tf.image.resize(tf.image.convert_image_dtype(x, tf.float32), TAMANIO_IMAGEN), y),
        num_parallel_calls=tf.data.AUTOTUNE,
    )
    if entrenando:
        ds = ds.shuffle(1024, seed=SEMILLA, reshuffle_each_iteration=True)
    return ds.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

entrenamiento = preparar(seleccionar(idx_train), entrenando=True)
validacion = preparar(seleccionar(idx_val))
prueba = preparar(seleccionar(idx_test))

# Pruebas rápidas de integridad.
x_lote, y_lote = next(iter(validacion))
assert x_lote.shape[1:] == (224, 224, 3)
assert 0 <= int(tf.reduce_min(y_lote)) and int(tf.reduce_max(y_lote)) < 5
assert len(set(idx_train) & set(idx_val)) == len(set(idx_train) & set(idx_test)) == 0
print(info)
print(manifiesto.groupby(["split", "label"]).size().unstack(fill_value=0))
'''

EDA = r'''
# ADAPTADO: mosaico e histograma del conjunto de datos
fig, axes = plt.subplots(2, 5, figsize=(15, 6))
for ax, (imagen, etiqueta) in zip(axes.flat, tfds.as_numpy(dataset_base.take(10))):
    ax.imshow(imagen)
    ax.set_title(CLASES[int(etiqueta)])
    ax.axis("off")
fig.tight_layout()
fig.savefig(RAIZ / "figures" / "mosaico_dataset.png", dpi=180, bbox_inches="tight")
plt.show()

conteos = manifiesto.groupby(["split", "label"]).size().reset_index(name="imagenes")
conteos["clase"] = conteos["label"].map(dict(enumerate(CLASES)))
plt.figure(figsize=(11, 5))
sns.barplot(data=conteos, x="clase", y="imagenes", hue="split")
plt.title("Distribución estratificada de tf_flowers")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig(RAIZ / "figures" / "histograma_clases_splits.png", dpi=180)
plt.show()
'''


def architecture(model):
    heads = {
        "A": 'salida = Dense(5, activation="softmax", name="salida_5_clases")(x)',
        "B": 'x = Dense(256, activation="relu", name="densa_256")(x)\nsalida = Dense(5, activation="softmax", name="salida_5_clases")(x)',
        "C": 'x = Dense(512, activation="relu", name="densa_512")(x)\nx = Dropout(0.5, name="dropout_50")(x)\nx = Dense(128, activation="relu", name="densa_128")(x)\nsalida = Dense(5, activation="softmax", name="salida_5_clases")(x)',
    }
    return r'''
# 2. Cargar VGG16 con pesos entrenados en ImageNet
vgg16 = VGG16(weights="imagenet", include_top=False, input_shape=(224, 224, 3))

# 3. Congelar los pesos VGG16: sección convolucional SIN MODIFICACIONES
vgg16.trainable = False

# 4. Agregar el clasificador del MODELO_MODEL
entrada = tf.keras.Input(shape=(224, 224, 3), name="imagen_RGB")
x = aumento(entrada)
x = preprocess_input(x * 255.0)
x = vgg16(x, training=False)
x = GlobalAveragePooling2D(name="promedio_global")(x)
HEAD
modelo = Model(entrada, salida, name="VGG16_Modelo_MODEL")
assert not vgg16.trainable and all(not capa.trainable for capa in vgg16.layers)
modelo.summary()

with open(RAIZ / "results" / "modelo_MODEL_summary.txt", "w") as archivo:
    modelo.summary(print_fn=lambda linea: archivo.write(linea + "\n"))

# Diagrama pedagógico parecido al proporcionado: backbone fijo y cabezal variable.
fig, ax = plt.subplots(figsize=(14, 4))
ax.axis("off")
bloques = [
    ("Entrada\n224×224×3", "#d9edf7", 1.3),
    ("VGG16 convolucional\nCONGELADA\n14,714,688 parámetros", "#7fcdbb", 3.2),
    ("GlobalAveragePooling2D\n7×7×512 → 512", "#c7e9c0", 2.4),
] + HEAD_BLOCKS
x0 = 0
for texto, color, ancho in bloques:
    ax.add_patch(plt.Rectangle((x0, 0.8), ancho, 1.5, facecolor=color, edgecolor="black"))
    ax.text(x0 + ancho/2, 1.55, texto, ha="center", va="center", fontsize=9)
    x0 += ancho + 0.45
    if x0 < sum(b[2] + 0.45 for b in bloques):
        ax.annotate("", xy=(x0, 1.55), xytext=(x0-0.45, 1.55), arrowprops={"arrowstyle":"->"})
ax.set_xlim(-0.2, x0)
ax.set_ylim(0.4, 2.7)
ax.set_title("Modelo MODEL: solo cambia el cabezal clasificador", fontweight="bold")
fig.tight_layout()
fig.savefig(RAIZ / "figures" / "arquitectura_modelo_MODEL.png", dpi=220, bbox_inches="tight")
plt.show()
'''.replace("HEAD_BLOCKS", repr({
        "A": [("Dense 5\nSoftmax", "#fdae6b", 1.7)],
        "B": [("Dense 256\nReLU", "#fdd0a2", 1.7), ("Dense 5\nSoftmax", "#fdae6b", 1.7)],
        "C": [("Dense 512\nReLU", "#fdd0a2", 1.7), ("Dropout\n0.5", "#f7f7f7", 1.4), ("Dense 128\nReLU", "#fdd0a2", 1.7), ("Dense 5\nSoftmax", "#fdae6b", 1.7)],
    }[model])).replace("HEAD", heads[model]).replace("MODEL", model)


def train_cell(model):
    return r'''
# 5. Compilar
modelo.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)
ruta_pesos = RAIZ / "weights" / "modelo_MODEL_best.weights.h5"
callbacks = [
    tf.keras.callbacks.ModelCheckpoint(ruta_pesos, monitor="val_loss", save_best_only=True, save_weights_only=True),
    tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True),
    tf.keras.callbacks.ReduceLROnPlateau(monitor="val_loss", patience=2, factor=0.5, min_lr=1e-6),
]

# 6. Entrenar únicamente el nuevo clasificador
inicio = time.time()
historia = modelo.fit(entrenamiento, validation_data=validacion, epochs=EPOCAS, callbacks=callbacks)
duracion = time.time() - inicio
assert all(not capa.trainable for capa in vgg16.layers)

# 7. Guardar modelo, pesos, historial y configuración
modelo.load_weights(ruta_pesos)
ruta_modelo = RAIZ / "weights" / "modelo_MODEL.keras"
modelo.save(ruta_modelo)
historial = pd.DataFrame(historia.history)
historial.to_csv(RAIZ / "results" / "modelo_MODEL_historial.csv", index=False)
metadata = {
    "modelo": "MODEL", "semilla": SEMILLA, "dataset": "tf_flowers:3.0.1",
    "clases": CLASES, "mejor_epoca": int(historial["val_loss"].idxmin() + 1),
    "duracion_segundos": duracion,
    "parametros_totales": int(modelo.count_params()),
    "parametros_entrenables": int(sum(np.prod(v.shape) for v in modelo.trainable_weights)),
}
for ruta in [ruta_pesos, ruta_modelo]:
    metadata[ruta.name + "_sha256"] = hashlib.sha256(ruta.read_bytes()).hexdigest()
(RAIZ / "results" / "modelo_MODEL_metadata.json").write_text(json.dumps(metadata, indent=2))

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].plot(historial["loss"], label="entrenamiento")
axes[0].plot(historial["val_loss"], label="validación")
axes[0].set(title="Loss Modelo MODEL", xlabel="Época", ylabel="Loss")
axes[1].plot(historial["accuracy"], label="entrenamiento")
axes[1].plot(historial["val_accuracy"], label="validación")
axes[1].set(title="Accuracy Modelo MODEL", xlabel="Época", ylabel="Accuracy")
for ax in axes: ax.legend(); ax.grid(alpha=.25)
fig.tight_layout()
fig.savefig(RAIZ / "figures" / "curvas_modelo_MODEL.png", dpi=180)
plt.show()

# Verificación de recarga y predicción
recargado = tf.keras.models.load_model(ruta_modelo)
assert recargado.predict(x_lote[:1], verbose=0).shape == (1, 5)
print(json.dumps(metadata, indent=2))
'''.replace("MODEL", model)


TEST_IMPORTS = r'''
# ADAPTADO: evaluación completa multiclase
%pip -q install --upgrade "tensorflow-datasets>=4.9,<5.0" "scikit-learn>=1.6,<2.0" seaborn==0.13.2
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
import tensorflow_datasets as tfds
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix,
    precision_recall_fscore_support
)
from sklearn.model_selection import train_test_split

SEMILLA = 42
TAMANIO_IMAGEN = (224, 224)
BATCH_SIZE = 16
RAIZ = Path.cwd()
for carpeta in ["data", "results", "figures", "weights"]:
    (RAIZ / carpeta).mkdir(exist_ok=True)
'''

TEST_DATA = r'''
# Cargar exactamente el mismo conjunto y reconstruir la partición de prueba
dataset_base, info = tfds.load(
    "tf_flowers:3.0.1", split="train", as_supervised=True,
    with_info=True, shuffle_files=False
)
CLASES = list(info.features["label"].names)
TOTAL = info.splits["train"].num_examples
etiquetas = np.fromiter((int(y) for _, y in tfds.as_numpy(dataset_base)), dtype=np.int64, count=TOTAL)
indices = np.arange(TOTAL, dtype=np.int64)
idx_train, idx_temp, y_train, y_temp = train_test_split(
    indices, etiquetas, test_size=0.30, random_state=SEMILLA, stratify=etiquetas
)
idx_val, idx_test, y_val, y_test = train_test_split(
    idx_temp, y_temp, test_size=0.50, random_state=SEMILLA, stratify=y_temp
)
def crear_split(indices_split):
    llaves = tf.constant(indices_split, dtype=tf.int64)
    tabla = tf.lookup.StaticHashTable(
        tf.lookup.KeyValueTensorInitializer(llaves, tf.ones_like(llaves, dtype=tf.int32)), 0
    )
    sin_batch = dataset_base.enumerate().filter(
        lambda i, elemento: tabla.lookup(i) > 0
    ).map(lambda i, elemento: elemento)
    preparado = sin_batch.map(
        lambda x, y: (tf.image.resize(tf.image.convert_image_dtype(x, tf.float32), TAMANIO_IMAGEN), y),
        num_parallel_calls=tf.data.AUTOTUNE
    ).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
    return sin_batch, preparado

validacion_sin_batch, validacion = crear_split(idx_val)
prueba_sin_batch, prueba = crear_split(idx_test)
'''


def test_eval(model):
    return (r'''
# Cargar el modelo guardado por el Colab Train correspondiente
ruta_modelo = RAIZ / "weights" / "modelo_MODEL.keras"
if not ruta_modelo.exists():
    raise FileNotFoundError("Ejecuta primero VGG16_Modelo_MODEL_Train.ipynb y coloca sus artefactos en weights/.")
modelo = tf.keras.models.load_model(ruta_modelo)

# Predicciones sobre TODO el conjunto de prueba
y_real = np.concatenate([y.numpy() for _, y in prueba])
probabilidades = modelo.predict(prueba, verbose=1)
y_pred = probabilidades.argmax(axis=1)
confianza = probabilidades.max(axis=1)
assert len(y_real) == len(idx_test) and probabilidades.shape == (len(y_real), 5)
y_val_real = np.concatenate([y.numpy() for _, y in validacion])
y_val_pred = modelo.predict(validacion, verbose=0).argmax(axis=1)
_, _, f1_validacion, _ = precision_recall_fscore_support(
    y_val_real, y_val_pred, average="macro", zero_division=0
)

predicciones = pd.DataFrame({
    "index": np.sort(idx_test), "real": y_real, "predicha": y_pred,
    "clase_real": [CLASES[i] for i in y_real],
    "clase_predicha": [CLASES[i] for i in y_pred],
    "confianza": confianza,
})
for i, clase in enumerate(CLASES):
    predicciones[f"p_{clase}"] = probabilidades[:, i]
predicciones.to_csv(RAIZ / "results" / "modelo_MODEL_predicciones.csv", index=False)

cm = confusion_matrix(y_real, y_pred, labels=range(5))
cm_norm = confusion_matrix(y_real, y_pred, labels=range(5), normalize="true")
precision, recall, f1, soporte = precision_recall_fscore_support(
    y_real, y_pred, labels=range(5), zero_division=0
)
tn = cm.sum() - (cm.sum(axis=0) + cm.sum(axis=1) - np.diag(cm))
fp = cm.sum(axis=0) - np.diag(cm)
fn = cm.sum(axis=1) - np.diag(cm)
tp = np.diag(cm)
por_clase = pd.DataFrame({
    "clase": CLASES, "TP": tp, "TN": tn, "FP": fp, "FN": fn,
    "precision": precision, "recall": recall, "f1": f1, "soporte": soporte,
})
por_clase.to_csv(RAIZ / "results" / "modelo_MODEL_metricas_por_clase.csv", index=False)
pd.DataFrame(cm, index=CLASES, columns=CLASES).to_csv(RAIZ / "results" / "modelo_MODEL_matriz_confusion.csv")
pd.DataFrame(cm_norm, index=CLASES, columns=CLASES).to_csv(RAIZ / "results" / "modelo_MODEL_matriz_confusion_normalizada.csv")

p_macro, r_macro, f_macro, _ = precision_recall_fscore_support(y_real, y_pred, average="macro", zero_division=0)
p_weighted, r_weighted, f_weighted, _ = precision_recall_fscore_support(y_real, y_pred, average="weighted", zero_division=0)
metricas = {
    "modelo": "MODEL", "accuracy": accuracy_score(y_real, y_pred),
    "precision_macro": p_macro, "recall_macro": r_macro, "f1_macro": f_macro,
    "precision_weighted": p_weighted, "recall_weighted": r_weighted, "f1_weighted": f_weighted,
    "f1_macro_validacion": f1_validacion,
    "brecha_f1_validacion_prueba": abs(f1_validacion - f_macro),
}
assert np.isclose(metricas["accuracy"], np.trace(cm) / cm.sum())
for i in range(5):
    assert np.isclose(precision[i], tp[i] / (tp[i] + fp[i]) if tp[i] + fp[i] else 0)
    assert np.isclose(recall[i], tp[i] / (tp[i] + fn[i]) if tp[i] + fn[i] else 0)
(RAIZ / "results" / "modelo_MODEL_metricas.json").write_text(json.dumps(metricas, indent=2))
(RAIZ / "results" / "modelo_MODEL_classification_report.txt").write_text(
    classification_report(y_real, y_pred, target_names=CLASES, zero_division=0)
)
print(json.dumps(metricas, indent=2))
display(por_clase)
''').replace("MODEL", model)


def test_figures(model):
    return r'''
# Matriz de confusión absoluta y normalizada
fig, axes = plt.subplots(1, 2, figsize=(15, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=CLASES, yticklabels=CLASES, ax=axes[0])
axes[0].set(title="Matriz de confusión — Modelo MODEL", xlabel="Predicción", ylabel="Observación")
sns.heatmap(cm_norm, annot=True, fmt=".2f", cmap="Greens", xticklabels=CLASES, yticklabels=CLASES, ax=axes[1])
axes[1].set(title="Matriz normalizada — Modelo MODEL", xlabel="Predicción", ylabel="Observación")
for ax in axes: ax.tick_params(axis="x", rotation=30)
fig.tight_layout()
fig.savefig(RAIZ / "figures" / "matrices_confusion_modelo_MODEL.png", dpi=190)
plt.show()

# Precision, Recall y F1 por clase
por_clase.set_index("clase")[["precision", "recall", "f1"]].plot(kind="bar", figsize=(11, 5), ylim=(0, 1))
plt.title("Métricas por clase — Modelo MODEL")
plt.ylabel("Valor"); plt.xticks(rotation=20); plt.grid(axis="y", alpha=.25); plt.tight_layout()
plt.savefig(RAIZ / "figures" / "metricas_clase_modelo_MODEL.png", dpi=180)
plt.show()

# Histograma de confianza de aciertos y errores
predicciones["resultado"] = np.where(y_real == y_pred, "Correcta", "Incorrecta")
plt.figure(figsize=(9, 5))
sns.histplot(data=predicciones, x="confianza", hue="resultado", bins=20, multiple="layer")
plt.title("Confianza de predicciones — Modelo MODEL")
plt.xlim(0, 1); plt.tight_layout()
plt.savefig(RAIZ / "figures" / "histograma_confianza_modelo_MODEL.png", dpi=180)
plt.show()
'''.replace("MODEL", model)


def single_image(model):
    return r'''
# Validación de una imagen individual (adaptación del Colab Test original)
# Cambia la ruta si deseas usar tu propia imagen; si no existe, se usa una imagen de prueba.
ruta_imagen = RAIZ / "imagen_prueba.jpg"
if ruta_imagen.exists():
    imagen = tf.keras.utils.load_img(ruta_imagen, target_size=TAMANIO_IMAGEN)
    imagen = tf.keras.utils.img_to_array(imagen) / 255.0
    imagen_mostrar = imagen
else:
    imagen_tensor, etiqueta_real = next(iter(prueba_sin_batch))
    imagen_mostrar = imagen_tensor.numpy()
    imagen = tf.image.resize(tf.image.convert_image_dtype(imagen_tensor, tf.float32), TAMANIO_IMAGEN).numpy()
imagen_lote = np.expand_dims(imagen, axis=0)
probs = modelo.predict(imagen_lote, verbose=0)[0]
predicha = int(np.argmax(probs))
plt.imshow(np.clip(imagen_mostrar, 0, 255).astype("uint8"))
plt.title(f"Modelo MODEL: {CLASES[predicha]} ({probs[predicha]:.2%})")
plt.axis("off"); plt.show()
print("Clase predicha:", CLASES[predicha])
print(pd.Series(probs, index=CLASES, name="probabilidad").sort_values(ascending=False))

# Si ya existen resultados de los tres modelos, crear comparación y ranking.
rutas = [RAIZ / "results" / f"modelo_{m}_metricas.json" for m in "ABC"]
if all(r.exists() for r in rutas):
    comparacion = pd.DataFrame([json.loads(r.read_text()) for r in rutas])
    for i, fila in comparacion.iterrows():
        meta = json.loads((RAIZ / "results" / f"modelo_{fila['modelo']}_metadata.json").read_text())
        comparacion.loc[i, "parametros_entrenables"] = meta["parametros_entrenables"]
    comparacion.to_csv(RAIZ / "results" / "comparacion_modelos.csv", index=False)
    orden = comparacion.sort_values(
        ["f1_macro", "accuracy", "brecha_f1_validacion_prueba", "parametros_entrenables"],
        ascending=[False, False, True, True],
    )
    ganador = orden.iloc[0]
    resumen = (
        f"El Modelo {ganador['modelo']} obtuvo el mayor F1 macro "
        f"({ganador['f1_macro']:.4f}) y Accuracy {ganador['accuracy']:.4f}."
    )
    (RAIZ / "results" / "ganador.txt").write_text(resumen)
    comparacion.set_index("modelo")[["accuracy", "precision_macro", "recall_macro", "f1_macro"]].plot(
        kind="bar", figsize=(10, 5), ylim=(0, 1)
    )
    plt.title("Comparación de los tres modelos"); plt.ylabel("Valor")
    plt.xticks(rotation=0); plt.grid(axis="y", alpha=.25); plt.tight_layout()
    plt.savefig(RAIZ / "figures" / "comparacion_modelos.png", dpi=190)
    plt.show()
    print(resumen)
'''.replace("MODEL", model)


def notebook(cells):
    return {
        "cells": cells,
        "metadata": {
            "accelerator": "GPU",
            "colab": {"name": "VGG16 tf_flowers", "provenance": []},
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def main():
    NB_DIR.mkdir(parents=True, exist_ok=True)
    for model in "ABC":
        train = notebook([
            markdown(f"# CNN–VGG16 — Modelo {model} (Train)\n\nVariación directa de `VGG16_Train.ipynb`. La sección convolucional no se modifica."),
            code(SETUP), code(DATA), code(EDA), code(architecture(model)), code(train_cell(model)),
        ])
        test = notebook([
            markdown(f"# CNN–VGG16 — Modelo {model} (Test)\n\nVariación directa de `VGG16_Test.ipynb`: evaluación completa y predicción individual."),
            code(TEST_IMPORTS), code(TEST_DATA), code(test_eval(model)), code(test_figures(model)), code(single_image(model)),
        ])
        for suffix, content in [("Train", train), ("Test", test)]:
            path = NB_DIR / f"VGG16_Modelo_{model}_{suffix}.ipynb"
            path.write_text(json.dumps(content, ensure_ascii=False, indent=1) + "\n")
            print(path)


if __name__ == "__main__":
    main()
