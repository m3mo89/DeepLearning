## Why

El reporte describe las arquitecturas implementadas, pero todavía no reúne en una explicación pedagógica completa el propósito de la semilla fija, el sobreajuste, la elección de `GlobalAveragePooling2D` frente a `Flatten`, la lógica conjunta de los tres modelos y las alternativas que quedaron fuera del alcance. Incorporar esas razones permitirá que el lector entienda tanto qué se hizo como por qué se diseñó así el experimento, sin confundir decisiones controladas con supuestos de superioridad universal.

## What Changes

- Ampliar la explicación de la semilla fija para cubrir reproducibilidad, comparación justa, fuentes de aleatoriedad y las limitaciones de una sola ejecución.
- Definir sobreajuste, subajuste y brecha de generalización, y relacionarlos con las curvas y medidas preventivas usadas en el experimento.
- Explicar cuantitativa y conceptualmente por qué se utilizó `GlobalAveragePooling2D` en lugar de `Flatten`, incluyendo dimensiones, parámetros, costo, invariancia espacial y pérdida de detalle espacial.
- Presentar A, B y C como una escala experimental controlada de capacidad mínima, intermedia y profunda regularizada.
- Complementar las definiciones existentes de `Dense` y `Dropout` con sus funciones respectivas y evitar presentarlas como tecnologías intercambiables.
- Incorporar una tabla de opciones alternativas —pooling, convoluciones, atención, clasificadores externos, fine-tuning y regularizaciones— con ventajas potenciales y motivos para no evaluarlas.
- Justificar que esas opciones quedaron fuera del alcance para preservar el aislamiento de variables y evitar una búsqueda combinatoria de hiperparámetros que requeriría múltiples semillas.
- Conservar intactos los notebooks, arquitecturas, pesos, configuración, métricas, figuras de resultados y conclusión experimental.

## Capabilities

### New Capabilities

Ninguna.

### Modified Capabilities

- `model-architecture-pedagogy`: ampliar los requisitos explicativos del reporte para cubrir reproducibilidad, sobreajuste, pooling frente a `Flatten`, lógica de selección de las tres variantes y alternativas no evaluadas.

## Impact

El cambio afecta principalmente `vgg16_tf_flowers/report/main.tex` y el PDF compilado. Puede requerir validar los paquetes LaTeX usados por la nueva tabla y regenerar `main.pdf` y `reporte_vgg16.pdf`; no modifica código de entrenamiento, dependencias de Python, artefactos de modelos ni resultados experimentales.
