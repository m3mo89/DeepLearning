## ADDED Requirements

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
