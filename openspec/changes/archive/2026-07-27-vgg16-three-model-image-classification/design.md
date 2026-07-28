## Context

Los notebooks entregados cargan imágenes desde directorios, usan VGG16 preentrenada con `include_top=False`, congelan sus capas, aplican `GlobalAveragePooling2D` y terminan en una única neurona `sigmoid`. Ese punto de partida sirve para dos clases, pero la actividad exige al menos tres, tres variaciones justificadas del clasificador, evaluación completa, pesos y un reporte LaTeX.

La entrega conservará el formato pedagógico del profesor: habrá un Colab de entrenamiento y otro de prueba para cada variante. Los seis notebooks serán copias adaptadas de las plantillas originales, no una reescritura con una arquitectura de software distinta. Se conservarán, cuando sigan siendo correctos, el orden de secciones, nombres conceptuales y comentarios; las líneas nuevas o modificadas se señalarán con comentarios breves.

Se selecciona `tf_flowers` porque es público, está integrado en TensorFlow Datasets, contiene 3,670 imágenes RGB de cinco clases y puede ejecutarse razonablemente en Google Colab. Solo ofrece un split `train`, por lo que la solución debe crear y registrar sus propias particiones sin fuga de datos.

## Goals / Non-Goals

**Goals:**

- Producir un experimento reproducible y justo para tres cabezales densos sobre el mismo extractor VGG16 congelado.
- Adaptar correctamente el ejemplo binario a clasificación multiclase mediante cinco salidas `softmax` y `sparse_categorical_crossentropy`.
- Generar todos los artefactos que necesita el reporte: métricas, matrices de confusión, curvas, histogramas, diagramas, tablas y pesos.
- Permitir ejecutar entrenamiento y evaluación en Colab y reconstruir el reporte localmente o en Overleaf.
- Entregar seis Colabs autónomos, dos por modelo, reconocibles como variaciones directas de los notebooks proporcionados.
- Elegir el modelo ganador con una regla explícita basada principalmente en F1 macro sobre prueba.

**Non-Goals:**

- Modificar, descongelar o afinar las capas convolucionales de VGG16.
- Comparar VGG16 contra otras familias de CNN.
- Buscar exhaustivamente hiperparámetros o afirmar rendimiento de estado del arte.
- Inventar resultados antes de ejecutar los tres entrenamientos.
- Usar el conjunto de prueba para seleccionar épocas o hiperparámetros.

## Decisions

### Dataset y particiones

Se cargará `tf_flowers:3.0.1` mediante TFDS y se generará un manifiesto determinista, estratificado por clase, con 70% entrenamiento, 15% validación y 15% prueba, semilla global 42. El manifiesto guardará identificadores/índices y etiquetas para que los tres modelos vean exactamente los mismos ejemplos. La validación se usará para `EarlyStopping` y selección de pesos; prueba se evaluará una sola vez al final.

Se prefirió `tf_flowers` frente a CIFAR-10 porque sus imágenes naturales de tamaño variable se parecen más al escenario de transferencia de VGG16 y sus cinco clases mantienen costo manejable. Se descartó `cats_vs_dogs` porque solo tiene dos clases.

### Preprocesamiento común

Todas las imágenes se convertirán a RGB, se redimensionarán a 224×224 y pasarán por `tensorflow.keras.applications.vgg16.preprocess_input`. Se aplicará la misma aumentación moderada únicamente al entrenamiento (volteo horizontal, rotación y zoom pequeños). Validación y prueba no tendrán aumentación.

Se usará `tf.data` con `cache` cuando sea viable, `shuffle` solo en entrenamiento, lotes de 16 y `prefetch(AUTOTUNE)`. Las semillas de Python, NumPy y TensorFlow quedarán fijadas, y se activarán operaciones deterministas cuando el entorno lo permita.

### Arquitectura compartida y cabezales

Los tres modelos usarán `VGG16(weights="imagenet", include_top=False, input_shape=(224,224,3))`, completamente congelada, seguida por `GlobalAveragePooling2D`. Así, la sección convolucional y el vector de 512 características serán idénticos.

- **Modelo A — línea base:** `Dense(5, softmax)`. Mide cuánto separables son las características ImageNet sin capacidad oculta adicional y minimiza sobreajuste.
- **Modelo B — capacidad intermedia:** `Dense(256, relu)` → `Dense(5, softmax)`. Permite aprender combinaciones no lineales con un incremento moderado de parámetros.
- **Modelo C — profundo regularizado:** `Dense(512, relu)` → `Dropout(0.5)` → `Dense(128, relu)` → `Dense(5, softmax)`. Prueba mayor capacidad mientras `Dropout` limita el sobreajuste esperado por el tamaño del dataset.

No se usará `Flatten`, porque produciría 25,088 características y muchos más parámetros densos; `GlobalAveragePooling2D` mantiene la comparación centrada en la variación neuronal con menor riesgo de sobreajuste.

### Protocolo de entrenamiento

Cada modelo se inicializará desde cero en su cabezal y se entrenará con Adam, tasa inicial 1e-3, `sparse_categorical_crossentropy`, máximo de 30 épocas y los mismos callbacks: `ModelCheckpoint(save_best_only=True)`, `EarlyStopping(patience=5, restore_best_weights=True)` y `ReduceLROnPlateau`. Se registrarán versión de dependencias, semilla, número de parámetros, tiempo, mejor época e historial completo.

La igualdad de datos, aumentación, optimizador, callbacks y presupuesto hace que la variable experimental principal sea el diseño del cabezal. Early stopping puede producir distintas cantidades de épocas, lo que se reportará como parte del resultado.

### Evaluación y selección

Las predicciones de prueba producirán una matriz de confusión 5×5. Se calcularán Accuracy y, para Precision, Recall y F1, valores por clase y promedios macro; también se guardará el promedio weighted como información complementaria. Se usará `zero_division=0` y se documentará la extensión multiclase de TP, FP, FN y TN mediante un esquema uno-contra-resto.

El ganador será el mayor F1 macro de prueba, porque pondera las cinco clases por igual. Accuracy será el primer desempate, seguido de menor brecha entre F1 macro de validación y prueba, y finalmente menor número de parámetros entrenables. No se concluirá cuál gana hasta contar con resultados reales.

### Visualizaciones y reporte

Cada arquitectura se exportará con `keras.utils.plot_model` y un resumen tabular de capas/parámetros. Se generarán: mosaico de ejemplos, histograma de imágenes por clase y split, curvas de loss/accuracy, matrices de confusión, barras comparativas de métricas, F1 por clase e histograma de confianza de predicciones correctas/incorrectas.

El reporte LaTeX incluirá portada, resumen, dataset, metodología, tres modelos y justificación, protocolo, fórmulas, resultados, discusión, conclusión, referencias y apéndice de reproducibilidad. Las tablas se alimentarán desde resultados reales exportados; quedarán marcadores evidentes si todavía no se ha entrenado, y la validación final rechazará marcadores pendientes.

### Estructura de entrega

La implementación separará notebooks, configuración, resultados, figuras, pesos y reporte. Los archivos principales serán `VGG16_Modelo_A_Train.ipynb`/`VGG16_Modelo_A_Test.ipynb`, equivalentes para B y C. Cada notebook `Train` preparará los mismos splits, construirá y entrenará solo su modelo y guardará sus pesos, historial y gráficas. Cada notebook `Test` reconstruirá o cargará únicamente el modelo correspondiente, evaluará todo el conjunto de prueba, calculará las métricas y matriz de confusión solicitadas, y conservará además la prueba de una imagen individual adaptada a cinco probabilidades `softmax`.

Cada modelo guardará el mejor archivo de pesos y un modelo final `.keras`, junto con hashes SHA-256 y un manifiesto. Se evitará ocultar la lógica esencial en módulos externos para que cada Colab pueda revisarse y ejecutarse por separado; la repetición controlada entre notebooks es aceptable en esta entrega académica. Un README indicará el orden Train→Test de cada modelo, entorno Colab, descarga de artefactos y compilación LaTeX.

## Risks / Trade-offs

- [El único split de TFDS puede causar fuga de datos] → Crear una partición estratificada una sola vez, persistir el manifiesto y reutilizarlo en todos los modelos.
- [No determinismo de GPU] → Fijar semillas, solicitar operaciones deterministas y documentar que pueden persistir pequeñas diferencias entre hardware/versiones.
- [El Modelo C puede sobreajustar] → Usar aumentación común, `Dropout`, early stopping y analizar brechas entrenamiento-validación.
- [F1 puede definirse de varias formas en multiclase] → Reportar por clase, macro y weighted, declarar F1 macro como métrica decisoria y no usar una fórmula binaria sin explicar uno-contra-resto.
- [Pesos y modelos pueden ocupar demasiado para Git] → Mantener un manifiesto con hashes y empaquetarlos para la entrega, usando Git LFS o almacenamiento externo solo si el repositorio lo requiere.
- [Colab puede interrumpir sesiones] → Guardar checkpoints e historiales después de cada modelo y permitir reanudar sin repetir modelos terminados.
- [Los resultados aún no existen durante la propuesta] → Prohibir números simulados y completar tablas/conclusión únicamente desde archivos generados por la evaluación.
