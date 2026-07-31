## Context

El reporte ya define `Dense`, ReLU, `softmax` y `Dropout`, justifica las unidades de cada modelo y señala que las variantes son independientes. Sin embargo, las razones metodológicas aparecen dispersas o implícitas: la semilla se menciona junto a la partición, `GlobalAveragePooling2D` se describe sin un contraste completo con `Flatten`, el sobreajuste se usa antes de ofrecer una definición integrada y falta una vista conjunta de las alternativas deliberadamente excluidas.

La ampliación debe ser comprensible para un lector principiante, técnicamente precisa y consistente con un experimento ya ejecutado. Las afirmaciones cuantitativas deben derivarse de las formas reales (`7×7×512` y 512 después del promedio global) y de las arquitecturas existentes. Ninguna explicación nueva puede insinuar que se entrenaron alternativas o que una única semilla establece superioridad estadística.

## Goals / Non-Goals

**Goals:**

- Explicar cómo una semilla fija favorece reproducibilidad y equidad comparativa, así como sus límites frente a múltiples semillas y diferencias de entorno.
- Definir sobreajuste, subajuste y brecha de generalización antes de usarlos como criterios de diseño o interpretación.
- Contrastar `GlobalAveragePooling2D` y `Flatten` con dimensiones, conteos aproximados de parámetros, ventajas y pérdida de información espacial.
- Presentar los tres modelos como una escala controlada de capacidad que responde preguntas experimentales distintas.
- Separar conceptualmente las capas que transforman características de las técnicas que regularizan el aprendizaje.
- Documentar alternativas plausibles y explicar por qué quedaron fuera del alcance sin calificarlas como inferiores.
- Mantener trazabilidad entre texto, código, resúmenes y resultados existentes.

**Non-Goals:**

- Modificar o volver a entrenar A, B o C.
- Probar `Flatten`, pooling máximo, convoluciones adicionales, atención, SVM, fine-tuning u otras regularizaciones.
- Realizar búsqueda de hiperparámetros, múltiples semillas o inferencia estadística nueva.
- Cambiar métricas, figuras de resultados, selección del ganador o conclusiones empíricas.

## Decisions

### Integrar las explicaciones en el flujo pedagógico existente

La definición de sobreajuste aparecerá en metodología, antes de justificar decisiones que lo reducen. La semilla se ampliará cerca de la partición y el protocolo; el contraste de pooling aparecerá al describir la salida de VGG16; y la lógica A–B–C precederá sus subsecciones individuales. Esto evita una sección aislada de preguntas frecuentes y permite que cada concepto aparezca antes de ser necesario.

### Explicar la semilla como control parcial, no como garantía absoluta

El reporte enumerará las fuentes de aleatoriedad controladas: partición, inicialización del cabezal, orden de lotes, aumentación y `Dropout`. También indicará que una semilla fija mejora la repetibilidad y garantiza particiones comunes, pero una sola ejecución no mide variabilidad y algunas operaciones pueden diferir entre hardware o versiones. Se evita el lenguaje de reproducibilidad perfecta.

### Usar una comparación cuantitativa para `Flatten`

El tensor `7×7×512` equivale a 25,088 valores con `Flatten`, mientras `GlobalAveragePooling2D` produce 512 sin parámetros. El reporte mostrará el impacto aproximado sobre los cabezales: A pasaría de 2,565 a 125,445 parámetros; B, de 132,613 a 6,424,069; y C, de 328,965 a 12,911,877. Se explicará que el promedio global reduce costo y dependencia de posiciones exactas, a cambio de descartar detalle espacial. Así, la decisión se presenta como un compromiso adecuado al alcance y tamaño del dataset, no como una regla universal.

### Definir sobreajuste mediante comportamiento observable

La explicación conectará memorización de particularidades con una brecha creciente entre entrenamiento y validación. Distinguirá subajuste, buen ajuste y sobreajuste, y señalará curvas de pérdida y exactitud como evidencia, sin diagnosticar automáticamente cualquier diferencia pequeña. Se relacionarán las mitigaciones ya existentes: backbone congelado, promedio global, aumentación, early stopping, menor complejidad y `Dropout` en C.

### Presentar A, B y C como una escalera experimental

A responderá si las características congeladas son linealmente separables; B, si una recombinación no lineal intermedia aporta valor; y C, si mayor profundidad y capacidad ayudan al incorporar regularización. Se conservará la aclaración de que 256, 512 y 128 son hipótesis de diseño, no óptimos hallados mediante búsqueda.

### Incorporar una tabla de alternativas no evaluadas

La tabla tendrá cuatro dimensiones conceptuales: alternativa, función, ventaja potencial y motivo de exclusión. Incluirá `Flatten`, `GlobalMaxPooling2D`, `Conv2D`, atención, SVM, fine-tuning, L2, `BatchNormalization`, label smoothing, MixUp/CutMix y tasas adicionales de `Dropout`. El texto circundante aclarará que no se probaron porque cambiar varias dimensiones impide atribución causal, cada opción necesita ajuste propio y una evaluación rigurosa multiplicaría entrenamientos y semillas.

Se prefiere una tabla comparativa a una enumeración extensa porque permite distinguir rápidamente alternativas arquitectónicas de alternativas de regularización. Se usará `tabularx` y `booktabs` si ya están disponibles; de lo contrario se añadirán solo al preámbulo LaTeX, sin introducir dependencias de Python.

## Risks / Trade-offs

- [El reporte puede crecer demasiado o repetir definiciones existentes] → Integrar y reorganizar el texto actual en vez de duplicarlo, manteniendo cada concepto en un único lugar principal.
- [Los conteos hipotéticos de `Flatten` pueden contener errores] → Verificarlos mediante las fórmulas de parámetros densos y contrastarlos con las dimensiones reales de VGG16.
- [La tabla puede desbordar la página] → Usar `tabularx`, texto conciso y tamaño tipográfico moderado; dividirla solo si la compilación lo exige.
- [El lector puede interpretar las alternativas como resultados] → Titularla explícitamente “alternativas no evaluadas” y evitar comparaciones de desempeño.
- [La semilla puede presentarse como garantía de reproducibilidad] → Documentar las fuentes residuales de no determinismo y la necesidad de múltiples semillas para conclusiones estadísticas.
- [La edición puede alterar hechos experimentales] → Validar arquitecturas, cifras, métricas, ausencia de marcadores y compilación del PDF sin regenerar entrenamientos.
