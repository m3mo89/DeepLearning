# model-architecture-pedagogy

## Purpose

Define how the report explains the model architectures (A, B, C) so that a reader
unfamiliar with the underlying layer concepts can understand what each architectural
choice does, why each neuron count was used, and how the models relate to one another
experimentally — without altering any implemented architecture, parameter count, or
result.

## Requirements

### Requirement: Common layer concepts are introduced before model comparison
El reporte SHALL definir antes de depender de ellos los conceptos de capa `Dense`, activación ReLU, activación `softmax` y `Dropout`, y SHALL distinguir entre una capa, su número de unidades y su función de activación.

#### Scenario: Reader reaches the model descriptions
- **WHEN** el lector comienza la sección que compara los modelos A, B y C
- **THEN** ya dispone de una explicación de qué calcula una capa densa, cómo ReLU introduce no linealidad, cómo `softmax` produce una distribución sobre clases y cómo `Dropout` regulariza el entrenamiento

### Requirement: Model A explanation connects the output to the classification problem
El reporte SHALL explicar que el Modelo A recibe las 512 características extraídas por VGG16 y usa `Dense(5, softmax)` porque el problema contiene exactamente cinco clases mutuamente excluyentes. También SHALL describir el efecto de no incluir una capa oculta y SHALL relacionarlo con su carácter de línea base.

#### Scenario: Model A architecture is explained
- **WHEN** el reporte presenta `Dense(5, softmax)` para el Modelo A
- **THEN** explica que cada una de las cinco neuronas produce evidencia para una clase, que `softmax` la convierte en probabilidades cuya suma es uno y que el cabezal aprende una separación lineal con 2,565 parámetros

### Requirement: Model B explanation distinguishes hidden capacity from output size
El reporte SHALL explicar que `Dense(256, relu)` es una capa oculta que combina una transformación densa de 256 unidades con ReLU, SHALL justificar 256 como una capacidad intermedia experimental y SHALL aclarar por qué `Dense(5, softmax)` continúa siendo la salida.

#### Scenario: Model B hidden layer is explained
- **WHEN** el lector revisa la arquitectura del Modelo B
- **THEN** el reporte describe cómo las 256 unidades recombinan las características de VGG16, cómo ReLU permite relaciones no lineales, cómo la capacidad adicional aumenta los parámetros y el riesgo de sobreajuste, y por qué 256 representa un punto intermedio frente a capas menores o iguales/mayores que las 512 entradas

#### Scenario: Model B output remains five-dimensional
- **WHEN** el reporte contrasta las 256 unidades ocultas con las cinco unidades de salida
- **THEN** aclara que 256 es un hiperparámetro de representación y cinco está fijado por el número de clases

### Requirement: Model C explanation covers depth, bottleneck, and regularization
El reporte SHALL explicar el efecto y la justificación experimental de `Dense(512, relu)`, `Dropout(0.5)`, `Dense(128, relu)` y `Dense(5, softmax)` dentro del Modelo C.

#### Scenario: Model C capacity and bottleneck are explained
- **WHEN** el reporte presenta las capas densas de 512 y 128 unidades
- **THEN** explica que 512 conserva la dimensión de entrada sin expandirla, que 128 comprime esa representación a una cuarta parte como cuello de botella y qué compromisos motivan esos valores frente a capas más pequeñas o más grandes

#### Scenario: Model C dropout is explained
- **WHEN** el reporte presenta `Dropout(0.5)`
- **THEN** explica que durante entrenamiento anula aleatoriamente aproximadamente la mitad de las activaciones, que no añade parámetros y que busca reducir coadaptación y sobreajuste

#### Scenario: Model C output is explained
- **WHEN** el reporte presenta la capa final del Modelo C
- **THEN** explica que la salida conserva cinco neuronas `softmax` porque la cantidad de clases no cambia con la profundidad del cabezal

### Requirement: Neuron counts are framed as constraints or experimental hyperparameters
El reporte SHALL distinguir la cantidad de neuronas fijada por el problema de las cantidades ocultas elegidas como hiperparámetros y SHALL explicar por qué se usó cada valor sin afirmar que sea universalmente óptimo.

#### Scenario: Reader compares all neuron counts
- **WHEN** el lector compara 5, 256, 512 y 128 neuronas
- **THEN** entiende que cinco está impuesto por las clases, mientras 256, 512 y 128 representan niveles deliberados de capacidad y compresión que solo podrían declararse óptimos tras una búsqueda de hiperparámetros no realizada

### Requirement: Experimental independence is explicit
El reporte SHALL declarar que los modelos A, B y C son variantes entrenadas independientemente y SHALL distinguir los pesos preentrenados compartidos conceptualmente de VGG16 de los pesos nuevos de cada cabezal.

#### Scenario: Reader asks whether B is based on trained A
- **WHEN** se explica la relación entre los modelos A y B
- **THEN** el reporte indica que B usa A como referencia comparativa de arquitectura, pero no carga ni continúa los pesos aprendidos por A

#### Scenario: Reader asks whether C continues A or B
- **WHEN** se explica la relación del Modelo C con A y B
- **THEN** el reporte indica que C es una tercera variante construida con el mismo backbone preentrenado congelado, pero con un cabezal nuevo inicializado y entrenado independientemente

#### Scenario: Meaning of starting from scratch is qualified
- **WHEN** el reporte utiliza la idea de que un modelo “parte desde cero”
- **THEN** limita esa expresión al cabezal clasificador y conserva la aclaración de que VGG16 parte de pesos de ImageNet

### Requirement: Explanatory change preserves experimental facts
La ampliación SHALL conservar las arquitecturas implementadas, los conteos de parámetros, la configuración experimental, las métricas obtenidas y la conclusión existente.

#### Scenario: Expanded report is validated
- **WHEN** se compara el reporte ampliado con los notebooks, resúmenes y resultados existentes
- **THEN** las arquitecturas siguen siendo A=`Dense(5, softmax)`, B=`Dense(256, relu)`→`Dense(5, softmax)` y C=`Dense(512, relu)`→`Dropout(0.5)`→`Dense(128, relu)`→`Dense(5, softmax)`, sin cambios en resultados

### Requirement: Fixed-seed purpose and limitations are explained
El reporte SHALL explicar que la semilla fija controla fuentes de aleatoriedad para mejorar la reproducibilidad y asegurar una comparación común entre A, B y C, y SHALL aclarar que una sola semilla no mide variabilidad ni garantiza resultados idénticos entre todo hardware y versión de software.

#### Scenario: Reader encounters seed 42
- **WHEN** el reporte presenta la partición o el protocolo con semilla 42
- **THEN** identifica al menos la partición, inicialización, orden de entrenamiento, aumentación y `Dropout` como fuentes aleatorias controladas, y entiende que la semilla no mejora por sí misma el desempeño

#### Scenario: Reader interprets a single run
- **WHEN** el reporte extrae conclusiones de la ejecución reproducida
- **THEN** advierte que demostrar estabilidad o significancia requeriría repetir cada arquitectura con varias semillas y resumir su variabilidad

### Requirement: Overfitting is defined before it supports design claims
El reporte SHALL definir sobreajuste como aprendizaje de particularidades del entrenamiento que no generalizan, SHALL distinguirlo de subajuste y buen ajuste, y SHALL relacionarlo con diferencias observables entre entrenamiento y validación sin tratar una brecha aislada como prueba automática.

#### Scenario: Reader reviews regularization rationale
- **WHEN** el reporte justifica menor complejidad, aumentación, `Dropout` o `EarlyStopping`
- **THEN** ya explica la brecha de generalización y cómo las curvas de pérdida y exactitud pueden evidenciar sobreajuste

#### Scenario: Reader compares fitting regimes
- **WHEN** el lector contrasta subajuste, buen ajuste y sobreajuste
- **THEN** puede distinguir bajo desempeño incluso en entrenamiento, desempeño consistente en datos nuevos y alto desempeño de entrenamiento con deterioro fuera de muestra

### Requirement: Global pooling is justified against Flatten
El reporte SHALL comparar `GlobalAveragePooling2D` con `Flatten` sobre la salida `7×7×512` de VGG16 y SHALL explicar dimensiones, impacto en parámetros, riesgo de sobreajuste y el compromiso de información espacial de ambas opciones.

#### Scenario: Reader asks why Flatten was not used
- **WHEN** el reporte presenta el paso de `7×7×512` a 512 características
- **THEN** explica que `Flatten` produciría 25,088 entradas, mientras el promedio global produce 512 sin parámetros, y cuantifica o ejemplifica el incremento correspondiente de parámetros densos

#### Scenario: Reader evaluates the pooling trade-off
- **WHEN** se justifica `GlobalAveragePooling2D`
- **THEN** el reporte indica que reduce costo y dependencia de la posición exacta a cambio de perder detalle espacial, sin afirmar que `Flatten` sea universalmente incorrecto

### Requirement: Three-model selection forms a controlled capacity comparison
El reporte SHALL presentar conjuntamente A, B y C como niveles deliberados de capacidad y SHALL expresar la pregunta experimental asociada con cada variante antes o junto a sus explicaciones individuales.

#### Scenario: Reader surveys the three architectures
- **WHEN** el lector comienza la comparación de modelos
- **THEN** entiende que A prueba separabilidad lineal, B añade capacidad no lineal intermedia y C prueba mayor profundidad con regularización, manteniendo constante el resto del protocolo

### Requirement: Layer alternatives and regularization alternatives are distinguished
El reporte SHALL distinguir las alternativas que transforman o agregan características de las técnicas que regularizan el entrenamiento, y SHALL evitar presentar `Dense` y `Dropout` como elementos con la misma función.

#### Scenario: Reader asks what could replace Dense or Dropout
- **WHEN** el reporte enumera opciones distintas a las implementadas
- **THEN** separa capas o clasificadores como convoluciones, atención y SVM de regularizaciones como L2, label smoothing, MixUp, CutMix y variaciones de `Dropout`

### Requirement: Unevaluated alternatives and scope rationale are transparent
El reporte SHALL incluir una tabla de alternativas no evaluadas con su función, ventaja potencial y motivo de exclusión, y SHALL declarar que su exclusión preservó una comparación controlada y limitó el costo experimental, no que dichas alternativas sean inferiores.

#### Scenario: Reader reviews alternative approaches
- **WHEN** el lector consulta la tabla de alternativas
- **THEN** encuentra pooling alternativo, `Flatten`, convoluciones, atención, clasificador externo, fine-tuning y regularizaciones adicionales claramente marcados como no evaluados

#### Scenario: Reader asks why alternatives were excluded
- **WHEN** el reporte explica el alcance
- **THEN** relaciona la exclusión con aislamiento de variables, hiperparámetros adicionales, costo combinatorio y necesidad de múltiples semillas para una comparación rigurosa

### Requirement: Expanded rationale preserves the completed experiment
La ampliación SHALL conservar los notebooks, arquitecturas, parámetros, configuración, pesos, métricas, figuras y conclusión existentes, y SHALL limitar las afirmaciones nuevas a explicaciones o cálculos derivados de hechos ya implementados.

#### Scenario: Report is rebuilt after the explanatory change
- **WHEN** se valida la entrega actualizada
- **THEN** no cambian los resultados ni el ganador, la tabla no presenta alternativas como entrenadas y el PDF compila sin marcadores pendientes
