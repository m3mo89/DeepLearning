## ADDED Requirements

### Requirement: Learning curves are interpretable
El reporte SHALL explicar qué representan las curvas de pérdida y exactitud de entrenamiento y validación, qué significa una época y cómo sus tendencias permiten detectar convergencia, sobreajuste y subajuste.

#### Scenario: Training and validation curves stay close while improving
- **WHEN** ambas curvas mejoran y mantienen una separación pequeña
- **THEN** el reporte identifica el patrón como evidencia compatible con aprendizaje y generalización, sin presentarlo por sí solo como garantía

#### Scenario: Training improves while validation degrades
- **WHEN** la pérdida de entrenamiento continúa bajando pero la pérdida de validación se estanca o aumenta
- **THEN** el reporte explica que la separación es un indicio de sobreajuste y la relaciona con la elección de la mejor época

### Requirement: Confusion matrices are explained and applied
El reporte SHALL explicar que las filas representan clases reales, las columnas clases predichas, la diagonal aciertos y las celdas externas confusiones. También SHALL distinguir conteos absolutos de proporciones normalizadas por clase real.

#### Scenario: Reader inspects a diagonal cell
- **WHEN** el lector observa una celda diagonal
- **THEN** puede interpretarla como ejemplos de una clase clasificados correctamente, en cantidad absoluta o proporción según la matriz

#### Scenario: Reader inspects an off-diagonal cell
- **WHEN** el lector observa una celda fuera de la diagonal
- **THEN** puede identificar qué clase real fue confundida con qué clase predicha y relacionarla con falsos negativos de la primera y falsos positivos de la segunda

### Requirement: Per-class metrics are explained
El reporte SHALL explicar Accuracy, Precision, Recall, F1 y soporte, junto con la diferencia entre resultados por clase y promedios macro y ponderado.

#### Scenario: Precision and recall differ for a class
- **WHEN** una clase presenta Precision y Recall diferentes
- **THEN** el reporte explica si predominan predicciones falsas de esa clase o ejemplos reales omitidos, y usa F1 como equilibrio entre ambas medidas

#### Scenario: Macro and weighted averages are compared
- **WHEN** el reporte presenta promedios macro y ponderado
- **THEN** explica que macro otorga el mismo peso a cada clase y weighted pondera por soporte, justificando F1 macro como criterio principal

### Requirement: Prediction-confidence histograms are explained cautiously
El reporte SHALL definir la confianza como la mayor probabilidad `softmax` de cada ejemplo, SHALL diferenciar la distribución de aciertos y errores y SHALL advertir que confianza alta no equivale a certeza ni demuestra calibración.

#### Scenario: Incorrect predictions have high confidence
- **WHEN** el histograma contiene errores cerca de una confianza de uno
- **THEN** el reporte los interpreta como equivocaciones seguras del modelo y no como evidencia de que esas predicciones sean correctas

#### Scenario: Correct and incorrect distributions overlap
- **WHEN** las distribuciones de aciertos y errores se superponen
- **THEN** el reporte explica que un umbral de confianza no separaría perfectamente ambos grupos

### Requirement: Every result figure has an actionable reading guide
El reporte SHALL acompañar curvas, matrices de confusión, métricas por clase, histogramas de confianza y comparación global con texto que indique qué se representa, qué patrón observar y qué límites tiene la interpretación.

#### Scenario: Reader encounters a result figure
- **WHEN** aparece una figura de resultados para A, B o C
- **THEN** la leyenda o el texto cercano ofrece una guía suficiente para interpretarla sin depender únicamente del nombre del archivo o del eje

### Requirement: Winner selection is evidence-based
El reporte SHALL explicar por qué A fue seleccionado pese a la capacidad adicional de B y C mediante la regla previa y los valores observados de F1 macro, Accuracy, brecha de generalización y parámetros.

#### Scenario: A is compared with B
- **WHEN** el reporte contrasta A y B
- **THEN** muestra que A obtuvo F1 macro 0.8799 frente a 0.8775, Accuracy 0.8802 frente a 0.8784, menor brecha validación–prueba y muchos menos parámetros, calificando la diferencia de desempeño como pequeña

#### Scenario: A is compared with C
- **WHEN** el reporte contrasta A y C
- **THEN** muestra que A obtuvo F1 macro 0.8799 frente a 0.8652, Accuracy 0.8802 frente a 0.8675 y menor brecha validación–prueba pese a que C usa Dropout y más parámetros

#### Scenario: More layers appear more powerful
- **WHEN** el lector supone que añadir capas, neuronas o Dropout debe mejorar el resultado
- **THEN** el reporte distingue capacidad de generalización y explica que más parámetros permiten funciones más complejas, pero no añaden datos ni garantizan una mejor frontera para características VGG16 ya discriminativas

#### Scenario: Statistical certainty is considered
- **WHEN** se interpreta la ventaja observada de A
- **THEN** el reporte la limita a la regla definida y a la ejecución disponible, sin afirmar significancia estadística en ausencia de múltiples semillas o intervalos de confianza
