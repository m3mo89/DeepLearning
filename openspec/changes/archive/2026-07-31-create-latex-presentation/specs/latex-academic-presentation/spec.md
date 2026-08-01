## ADDED Requirements

### Requirement: Reproducible LaTeX presentation
El proyecto SHALL incluir una presentación académica implementada en LaTeX Beamer, su PDF compilado y comandos documentados para regenerarlo desde el repositorio.

#### Scenario: Presentation is built
- **WHEN** se compila el fuente con el comando documentado
- **THEN** se produce un PDF panorámico 16:9 sin errores, referencias pendientes ni desbordamientos visibles

### Requirement: Presentation has a documented oral duration
La presentación SHALL contener dieciocho diapositivas de contenido y una diapositiva final de preguntas, con un guion temporal aproximado de 18–19 minutos.

#### Scenario: Presenter rehearses the expanded sequence
- **WHEN** se sigue el guion sin utilizar material de respaldo
- **THEN** cada diapositiva dispone de un tiempo aproximado y el total planificado se encuentra documentado aunque supere el límite original de 15 minutos

### Requirement: All model learning curves and confusion matrices are visible
La secuencia principal SHALL mostrar en diapositivas separadas las curvas de aprendizaje de A, B y C y una matriz de confusión legible para cada modelo.

#### Scenario: Audience reviews comparative evidence
- **WHEN** finaliza la comparación de métricas globales
- **THEN** puede observar la evolución entrenamiento--validación y los patrones de confusión de los tres modelos sin depender del reporte escrito

### Requirement: Full report architecture images are included
La secuencia principal SHALL incluir en diapositivas separadas las imágenes completas de las arquitecturas A, B y C utilizadas en el reporte.

#### Scenario: Audience reviews model construction
- **WHEN** termina la comparación tabular de cabezales
- **THEN** puede observar los cinco bloques congelados de VGG16, el promedio global y el cabezal específico de cada variante en las mismas imágenes del reporte

### Requirement: Final questions slide provides an appropriate visual close
La presentación SHALL terminar con una diapositiva de preguntas que incluya agradecimiento y un meme original, breve y académicamente apropiado relacionado con CNN, VGG16 o la conclusión sobre complejidad del modelo.

#### Scenario: Main presentation reaches its end
- **WHEN** concluye la diapositiva de resultados y limitaciones
- **THEN** aparece una diapositiva final de preguntas cuyo meme no depende de una imagen externa, no introduce afirmaciones técnicas nuevas y puede presentarse en aproximadamente 20–30 segundos

### Requirement: Narrative covers the complete experiment
La secuencia principal SHALL explicar objetivo, dataset, VGG16 congelada, promedio global, lógica y arquitectura de A/B/C, protocolo, métricas, resultados, análisis del ganador, conclusión y limitaciones.

#### Scenario: Audience follows the presentation
- **WHEN** se recorren las diapositivas principales en orden
- **THEN** la audiencia puede reconstruir qué se comparó, qué permaneció fijo, cómo se evaluó y por qué A fue seleccionado en esta ejecución

### Requirement: Slides remain visually legible
Cada diapositiva SHALL priorizar una idea principal, tipografía proyectable, contraste suficiente y figuras o tablas legibles, evitando párrafos largos y contenido equivalente a una página del reporte.

#### Scenario: Slide deck is reviewed at presentation scale
- **WHEN** el PDF se visualiza como diapositivas completas
- **THEN** títulos, cifras, leyendas y mensajes principales pueden leerse sin acercamiento y ningún elemento queda fuera del marco

### Requirement: Existing visual evidence is reused
La presentación SHALL reutilizar figuras reales del dataset, arquitecturas y evaluación cuando apoyen la narrativa, sin fabricar gráficas ni duplicar innecesariamente activos.

#### Scenario: Results slides are inspected
- **WHEN** una diapositiva muestra comparaciones, errores o distribuciones
- **THEN** la imagen procede de `vgg16_tf_flowers/figures/` o la cifra puede rastrearse a los resultados exportados

### Requirement: Metrics and claims match completed results
La presentación SHALL conservar las métricas, parámetros, clases y conclusión del experimento completado, y SHALL distinguir el ganador de esta ejecución de una afirmación de superioridad universal.

#### Scenario: Presentation values are verified
- **WHEN** se contrastan sus cifras con `comparacion_modelos.csv`, métricas por clase y el reporte
- **THEN** A muestra Accuracy 0.8802, F1 macro 0.8799 y 2,565 parámetros entrenables; B muestra F1 macro 0.8775; C muestra F1 macro 0.8652; y no se afirma significancia estadística

### Requirement: Speaker guidance supports delivery
El proyecto SHALL incluir un guion breve que asigne tiempo, mensaje oral y transición a cada diapositiva principal sin exigir que el expositor lea texto completo.

#### Scenario: Presenter prepares the talk
- **WHEN** consulta el guion antes de ensayar
- **THEN** encuentra para cada diapositiva su propósito, duración aproximada, puntos que explicar y enlace narrativo con la siguiente

### Requirement: Presentation workflow is documented
El README SHALL indicar la ubicación del fuente, el PDF, el guion y el comando necesario para compilar la presentación.

#### Scenario: Another reader regenerates the slides
- **WHEN** sigue la sección correspondiente del README
- **THEN** puede localizar los archivos y compilar el PDF sin modificar resultados ni notebooks
