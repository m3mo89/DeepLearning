# Clasificación `tf_flowers` con tres modelos VGG16

**Autor:** Guillermo Tinoco Ramos

En este proyecto comparé tres clasificadores para el conjunto `tf_flowers` a
partir de los Colab `VGG16_Train.ipynb` y `VGG16_Test.ipynb` proporcionados en
clase. En los tres casos conservé la sección convolucional de VGG16 con pesos
de ImageNet y sin entrenamiento adicional. La diferencia entre los modelos se
encuentra únicamente en el cabezal clasificador.

## Archivos principales

| Modelo | Cabezal | Entrenamiento | Evaluación |
|---|---|---|---|
| A | `Dense(5, softmax)` | `notebooks/VGG16_Modelo_A_Train.ipynb` | `notebooks/VGG16_Modelo_A_Test.ipynb` |
| B | `Dense(256, relu) → Dense(5, softmax)` | `notebooks/VGG16_Modelo_B_Train.ipynb` | `notebooks/VGG16_Modelo_B_Test.ipynb` |
| C | `Dense(512, relu) → Dropout(0.5) → Dense(128, relu) → Dense(5, softmax)` | `notebooks/VGG16_Modelo_C_Train.ipynb` | `notebooks/VGG16_Modelo_C_Test.ipynb` |

## Prerrequisitos y preparación local

Preparé los notebooks para ejecutarlos principalmente en Google Colab. Para
usar las utilidades o reproducir el entorno localmente se necesita Python 3:

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
   a algunas horas según la GPU, la carga del servicio y el momento en que se
   active `EarlyStopping`.
6. Descarga `weights/`, `results/`, `figures/` y `data/split_manifest.csv`.

Si la carpeta tiene otro nombre o ubicación en Drive, modifica de forma
consistente la celda `%cd` y el valor `RAIZ_DRIVE` al inicio de cada notebook.
No basta con cambiar solo uno de los dos.

Si Colab se interrumpe después de terminar un modelo, los archivos guardados
permiten continuar con el siguiente. Cada notebook de prueba debe cargar los
pesos de su modelo correspondiente.

## Resultados producidos

Cada notebook de entrenamiento guarda los mejores pesos en formato
`.weights.h5`, el modelo `.keras`, el historial, los metadatos, los hashes, las
curvas y una imagen de la arquitectura. Cada notebook de prueba guarda:

- matriz de confusión absoluta y normalizada;
- TP, TN, FP y FN por clase;
- Accuracy, Precision, Recall y F1 por clase, además de los promedios macro y
  ponderado;
- probabilidades y etiquetas de cada ejemplo;
- gráficas de métricas e histograma de confianza;
- predicción de una imagen individual.

Después de evaluar los tres modelos se genera una comparación global. Utilicé
F1 macro como criterio principal porque asigna la misma importancia a las
cinco clases.

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

Las tablas, las métricas y la selección del modelo ganador se generan a partir
de los archivos JSON producidos durante la evaluación. De esta manera, el
contenido del reporte se puede relacionar directamente con las ejecuciones de
los notebooks.

## Presentación

La presentación se encuentra en `presentation/`. Incluye:

- `presentacion.tex`: fuente LaTeX Beamer en formato panorámico 16:9;
- `presentacion.pdf`: versión compilada para exponer;
- `guion.md`: tiempos, explicación oral y transiciones;
- `meme_modelo_a.png`: cierre visual de la diapositiva de preguntas.

Para compilarla con Tectonic:

```bash
cd presentation
tectonic presentacion.tex
```

El recorrido principal consta de dieciocho diapositivas de contenido y una de
preguntas. El guion suma aproximadamente 18 minutos 40 segundos e incluye las
arquitecturas del reporte, curvas y matrices de confusión de los tres modelos.

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
