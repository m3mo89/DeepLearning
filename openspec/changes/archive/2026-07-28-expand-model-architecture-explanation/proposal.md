## Why

El reporte identifica correctamente las capas y resultados de los modelos A, B y C, pero presupone que el lector ya entiende tanto los componentes de la red como la lectura de las visualizaciones y métricas. Se necesita una explicación gradual que conecte cada concepto, hiperparámetro, gráfica y resultado con la capacidad de generalización observada, incluida la razón por la cual el modelo más sencillo resultó ganador.

## What Changes

- Introducir los conceptos de capa `Dense` y activación `softmax` antes de presentar las tres variantes, incluyendo su función matemática e interpretación en clasificación multiclase.
- Ampliar el Modelo A para justificar la salida de cinco neuronas, explicar por qué `softmax` representa cinco clases mutuamente excluyentes y describir el efecto de usar un clasificador lineal sin capas ocultas.
- Ampliar el Modelo B para explicar el bloque `Dense(256) + ReLU`, la razón experimental de elegir 256 unidades, el motivo por el cual la salida continúa siendo `Dense(5, softmax)` y su relación con el Modelo A.
- Ampliar el Modelo C para explicar `Dense(512) + ReLU`, `Dropout(0.5)`, `Dense(128) + ReLU` y `Dense(5, softmax)`, justificando capacidad, regularización, cuello de botella y salida.
- Justificar por qué se eligieron 5, 256, 512 y 128 neuronas frente a otras cantidades, distinguiendo valores impuestos por el problema de hiperparámetros experimentales y evitando presentarlos como óptimos universales.
- Declarar explícitamente que A, B y C son experimentos independientes: comparten la arquitectura y los pesos congelados de VGG16, así como datos y configuración de entrenamiento, pero cada cabezal se inicializa y entrena desde cero; B no continúa A y C no continúa A ni B.
- Ampliar la lectura de curvas de pérdida y exactitud, matrices de confusión absoluta y normalizada, métricas por clase e histogramas de confianza.
- Explicar convergencia, sobreajuste, subajuste, ejes y diagonal de la matriz, falsos positivos y negativos, promedios macro y ponderado, y la diferencia entre confianza y certeza.
- Ampliar la comparación global y justificar con los resultados por qué A ganó aunque B y C tengan más capas y parámetros.
- Conservar las arquitecturas, resultados y conclusiones existentes; el cambio es explicativo y no altera el experimento.

## Capabilities

### New Capabilities

- `model-architecture-pedagogy`: Requisitos para que el reporte explique progresivamente las capas, activaciones, hiperparámetros y relación experimental entre los modelos A, B y C.
- `evaluation-results-pedagogy`: Requisitos para interpretar curvas, matrices de confusión, métricas por clase, histogramas de confianza y la selección del modelo ganador.

### Modified Capabilities

Ninguna.

## Impact

- Archivo principal afectado: `vgg16_tf_flowers/report/main.tex`, especialmente “Modelos propuestos”, “Métricas”, “Resultados”, “Discusión” y las leyendas de las figuras.
- Podrían regenerarse los artefactos PDF del reporte para validar composición, referencias y legibilidad.
- No cambian notebooks, código de entrenamiento, configuración, pesos, métricas, dependencias ni interfaces.
