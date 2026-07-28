## 1. Estructura y entorno reproducible

- [x] 1.1 Crear la estructura de directorios para notebooks/código, configuración, datos derivados, pesos, resultados, figuras y reporte.
- [x] 1.2 Definir dependencias versionadas para TensorFlow, TensorFlow Datasets, scikit-learn, NumPy, pandas, Matplotlib, Seaborn, pydot/Graphviz y herramientas LaTeX.
- [x] 1.3 Crear una configuración central con semilla 42, tamaño 224×224, batch 16, clases, hiperparámetros, rutas y variantes A/B/C.
- [x] 1.4 Implementar inicialización determinista y registro de versiones, hardware y configuración efectiva de cada ejecución.

## 2. Dataset y canalización de entrada

- [x] 2.1 Implementar la descarga/carga de `tf_flowers:3.0.1` mediante TFDS y registrar metadatos y nombres de sus cinco clases.
- [x] 2.2 Crear un manifiesto estratificado reproducible 70/15/15 y validar que no haya ejemplos duplicados ni fuga entre splits.
- [x] 2.3 Implementar los pipelines `tf.data` para entrenamiento, validación y prueba con resize RGB, aumentación exclusiva de entrenamiento, `preprocess_input`, batch y prefetch.
- [x] 2.4 Generar y guardar un mosaico de ejemplos y el histograma de distribución por clase y split.
- [x] 2.5 Añadir pruebas rápidas para tamaños de tensores, rango/etiquetas, estabilidad del manifiesto y ausencia de aumentación en evaluación.

## 3. Modelos VGG16

- [x] 3.1 Implementar una fábrica común con VGG16 ImageNet `include_top=False`, backbone congelado y `GlobalAveragePooling2D`.
- [x] 3.2 Implementar Modelo A con salida `Dense(5, softmax)` y validar parámetros entrenables.
- [x] 3.3 Implementar Modelo B con `Dense(256, relu)` y salida `Dense(5, softmax)`, y validar parámetros entrenables.
- [x] 3.4 Implementar Modelo C con `Dense(512, relu)`, `Dropout(0.5)`, `Dense(128, relu)` y salida `Dense(5, softmax)`, y validar parámetros entrenables.
- [x] 3.5 Añadir una comprobación automática de que todas las capas VGG16 permanecen congeladas antes y después del entrenamiento.
- [x] 3.6 Exportar `summary` y un diagrama legible por variante que muestre el backbone compartido y el cabezal específico.

## 4. Entrenamiento y persistencia

- [x] 4.1 Implementar entrenamiento común con Adam, `sparse_categorical_crossentropy`, máximo 30 épocas y métricas de seguimiento.
- [x] 4.2 Configurar checkpoints, early stopping y reducción de learning rate basados únicamente en validación.
- [x] 4.3 Entrenar el Modelo A y guardar mejor peso, modelo `.keras`, historial, mejor época, parámetros, duración y configuración.
- [x] 4.4 Entrenar el Modelo B y guardar mejor peso, modelo `.keras`, historial, mejor época, parámetros, duración y configuración.
- [x] 4.5 Entrenar el Modelo C y guardar mejor peso, modelo `.keras`, historial, mejor época, parámetros, duración y configuración.
- [x] 4.6 Calcular hashes SHA-256, construir el manifiesto de artefactos y verificar que cada modelo guardado pueda recargarse y predecir.

## 5. Evaluación y visualizaciones

- [x] 5.1 Implementar inferencia sobre prueba que guarde por ejemplo la etiqueta real, predicción y cinco probabilidades.
- [x] 5.2 Calcular para cada modelo Accuracy, Precision, Recall y F1 por clase, macro y weighted con `zero_division=0`.
- [x] 5.3 Calcular matrices de confusión 5×5 y validar las métricas contra TP, FP, FN y TN uno-contra-resto.
- [x] 5.4 Exportar métricas, reportes de clasificación y matrices numéricas en CSV/JSON con orden fijo de clases.
- [x] 5.5 Generar curvas de loss/accuracy, heatmaps de confusión, barras comparativas, F1 por clase e histogramas de confianza para aciertos y errores.
- [x] 5.6 Implementar el ranking por F1 macro, desempates definidos y generación automática del resumen justificativo del ganador.

## 6. Reporte LaTeX

- [x] 6.1 Crear la plantilla LaTeX con portada, resumen, dataset, metodología, modelos, métricas, resultados, discusión, conclusión, referencias y apéndice.
- [x] 6.2 Documentar `tf_flowers`, la partición estratificada, el preprocesamiento y las limitaciones del dataset con sus citas.
- [x] 6.3 Explicar VGG16 congelada y justificar por capacidad/regularización las neuronas de los modelos A, B y C.
- [x] 6.4 Incluir las fórmulas de Accuracy, Precision, Recall y F1, la matriz de confusión y la extensión multiclase uno-contra-resto.
- [x] 6.5 Integrar automáticamente diagramas, histogramas, curvas, matrices de confusión y tablas generadas desde resultados reales.
- [x] 6.6 Redactar el análisis por clase, sobreajuste, complejidad y errores, y completar la conclusión con el ganador calculado sin valores inventados.
- [x] 6.7 Compilar el PDF y corregir referencias, desbordamientos, figuras ilegibles, tablas incompletas y marcadores pendientes.

## 7. Notebooks y paquete final

- [x] 7.1 Crear `VGG16_Modelo_A_Train.ipynb` y `VGG16_Modelo_A_Test.ipynb` como variaciones mínimas y autónomas de los Colab proporcionados.
- [x] 7.2 Crear los pares Train/Test equivalentes para los modelos B y C, conservando la estructura de las plantillas y señalando las líneas adaptadas.
- [x] 7.3 Verificar que cada notebook Train entrene solo su variante, guarde sus pesos/historial/gráficas y pueda ejecutarse de principio a fin en Colab.
- [x] 7.4 Verificar que cada notebook Test cargue solo los pesos correspondientes, evalúe el conjunto de prueba completo y adapte la validación de una imagen a clase, confianza y cinco probabilidades.
- [x] 7.5 Crear README en español con orden Train→Test por modelo, activación de GPU, tiempos esperados, reanudación, descarga de pesos y compilación del reporte.
- [x] 7.6 Añadir un validador del paquete que compruebe los seis Colabs, configuraciones, tres pesos/modelos, hashes, métricas, figuras, fuentes LaTeX y PDF.
- [x] 7.7 Ejecutar los tres pares Train/Test desde entorno limpio o Colab, registrar cualquier desviación reproducible y corregir fallos.
- [x] 7.8 Construir el archivo final de entrega y verificar que abre, contiene todos los artefactos requeridos y no incluye secretos ni archivos temporales.
