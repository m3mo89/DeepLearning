# Clasificación `tf_flowers` con tres modelos VGG16

Entrega académica basada directamente en los Colab `VGG16_Train.ipynb` y
`VGG16_Test.ipynb` del profesor. La sección convolucional de VGG16 se conserva
con pesos ImageNet y permanece congelada. Solo cambian los cabezales densos.

## Archivos principales

| Modelo | Cabezal | Entrenamiento | Evaluación |
|---|---|---|---|
| A | `Dense(5, softmax)` | `notebooks/VGG16_Modelo_A_Train.ipynb` | `notebooks/VGG16_Modelo_A_Test.ipynb` |
| B | `Dense(256, relu) → Dense(5, softmax)` | `notebooks/VGG16_Modelo_B_Train.ipynb` | `notebooks/VGG16_Modelo_B_Test.ipynb` |
| C | `Dense(512, relu) → Dropout(0.5) → Dense(128, relu) → Dense(5, softmax)` | `notebooks/VGG16_Modelo_C_Train.ipynb` | `notebooks/VGG16_Modelo_C_Test.ipynb` |

## Prerrequisitos y preparación local

Los notebooks están preparados principalmente para Google Colab. Para ejecutar
las utilidades o reproducir el entorno localmente se necesita Python 3:

```bash
cd vgg16_tf_flowers
python3 -m pip install -r requirements.txt
```

Todos los comandos `python3 scripts/...` que aparecen más adelante se ejecutan
desde esta raíz `vgg16_tf_flowers/`. Para generar el PDF también se necesita
un compilador LaTeX: puede utilizarse `pdflatex` o Tectonic. Estas herramientas
no forman parte de `requirements.txt`.

## Ejecución en Google Colab

1. Sube el directorio completo a
   `/content/drive/MyDrive/vgg16_tf_flowers`. Los notebooks esperan exactamente
   esa ruta.
2. Abre Colab y selecciona **Entorno de ejecución → Cambiar tipo → GPU**.
3. Ejecuta `VGG16_Modelo_A_Train.ipynb` de principio a fin.
4. Sin cambiar la estructura de carpetas, ejecuta
   `VGG16_Modelo_A_Test.ipynb`.
5. Repite Train→Test para B y C. Cada Train puede tardar de decenas de minutos
   a algunas horas según GPU, carga del servicio y early stopping.
6. Descarga `weights/`, `results/`, `figures/` y `data/split_manifest.csv`.

Si la carpeta tiene otro nombre o ubicación en Drive, modifica de forma
consistente la celda `%cd` y el valor `RAIZ_DRIVE` al inicio de cada notebook.
No basta con cambiar solo uno de los dos.

Si Colab se interrumpe después de terminar un modelo, sus archivos guardados
permiten continuar con el siguiente. No se deben mezclar pesos entre modelos.

## Resultados producidos

Cada Train guarda el mejor `.weights.h5`, el modelo `.keras`, historial,
metadata, hashes, curvas y una imagen de arquitectura. Cada Test guarda:

- matriz de confusión absoluta y normalizada;
- TP, TN, FP y FN por clase;
- Accuracy, Precision, Recall y F1 por clase, macro y weighted;
- probabilidades y etiquetas de cada ejemplo;
- gráficas de métricas e histograma de confianza;
- predicción de una imagen individual.

Al completar los tres Test también se genera la comparación global y la
selección del ganador por F1 macro.

## Reporte

Después de copiar los resultados al proyecto, desde la raíz
`vgg16_tf_flowers/` genera primero las tablas y textos del reporte:

```bash
python3 scripts/build_report_assets.py
cd report
```

Con `pdflatex`, compila dos veces para resolver las referencias:

```bash
pdflatex -jobname=reporte_vgg16 main.tex
pdflatex -jobname=reporte_vgg16 main.tex
```

Como alternativa, Tectonic gestiona las repeticiones necesarias. Su salida
predeterminada se llama `main.pdf`, por lo que debe conservarse también con el
nombre requerido por la validación estricta:

```bash
tectonic main.tex
cp main.pdf reporte_vgg16.pdf
```

Ambos flujos deben dejar `report/reporte_vgg16.pdf`. El repositorio conserva
además `report/main.pdf` cuando se compila con Tectonic.

Escribe tu nombre en `report/main.tex` antes de entregar. El reporte no inventa
resultados: la tabla y el ganador provienen de los JSON generados.

## Validación y paquete

Desde la raíz `vgg16_tf_flowers/`, la validación estructural comprueba
notebooks, configuración, fuentes y README, pero no exige resultados de
entrenamiento:

```bash
python3 scripts/validate_submission.py
```

La validación estricta exige además los tres modelos, pesos, métricas, figuras,
hashes y `report/reporte_vgg16.pdf`:

```bash
python3 scripts/validate_submission.py --strict
```

Para validar y empaquetar en un solo paso:

```bash
python3 scripts/package_submission.py
```

El empaquetador ejecuta primero la validación estricta. Solo si todo está
completo y los hashes coinciden crea `VGG16_tf_flowers_entrega.zip` en el
directorio padre de `vgg16_tf_flowers/`.
