## ADDED Requirements

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
