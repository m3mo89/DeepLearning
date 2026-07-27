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

## Ejecución en Google Colab

1. Sube todo el directorio a Google Drive o conserva los notebooks y las
   carpetas `weights`, `results`, `figures` y `data` en el mismo directorio.
2. Abre Colab y selecciona **Entorno de ejecución → Cambiar tipo → GPU**.
3. Ejecuta `VGG16_Modelo_A_Train.ipynb` de principio a fin.
4. Sin cambiar la estructura de carpetas, ejecuta
   `VGG16_Modelo_A_Test.ipynb`.
5. Repite Train→Test para B y C. Cada Train puede tardar de decenas de minutos
   a algunas horas según GPU, carga del servicio y early stopping.
6. Descarga `weights/`, `results/`, `figures/` y `data/split_manifest.csv`.

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

Después de copiar los resultados al proyecto:

```bash
python3 scripts/build_report_assets.py
cd report
pdflatex -jobname=reporte_vgg16 main.tex
pdflatex -jobname=reporte_vgg16 main.tex
```

Escribe tu nombre en `report/main.tex` antes de entregar. El reporte no inventa
resultados: la tabla y el ganador provienen de los JSON generados.

## Validación y paquete

La estructura y sintaxis pueden revisarse antes del entrenamiento:

```bash
python3 scripts/validate_submission.py
```

La validación final exige los tres modelos, pesos, métricas, figuras y PDF:

```bash
python3 scripts/validate_submission.py --strict
python3 scripts/package_submission.py
```

El segundo comando crea `VGG16_tf_flowers_entrega.zip` solo si todo está
completo y los hashes coinciden.
