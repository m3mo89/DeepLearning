## Why

La actividad requiere una comparación reproducible de tres clasificadores multiclase basados en VGG16, conservando intacta su sección convolucional y variando únicamente el cabezal neuronal. El material de referencia entregado solo resuelve clasificación binaria y no genera las métricas, visualizaciones, pesos ni el reporte académico solicitados.

## What Changes

- Usar el conjunto público `tf_flowers` de TensorFlow Datasets, con 3,670 imágenes RGB y cinco clases.
- Construir una canalización reproducible con particiones estratificadas de entrenamiento, validación y prueba, redimensionamiento a 224×224 y preprocesamiento de VGG16.
- Implementar tres modelos que compartan VGG16 con pesos de ImageNet y capas convolucionales congeladas, y que difieran únicamente en sus capas densas:
  - Modelo A: clasificación lineal con salida `Dense(5, softmax)`.
  - Modelo B: `Dense(256, relu)` y salida `Dense(5, softmax)`.
  - Modelo C: `Dense(512, relu)`, `Dropout(0.5)`, `Dense(128, relu)` y salida `Dense(5, softmax)`.
- Entrenar los tres modelos bajo el mismo protocolo y guardar modelos, mejores pesos, historial, predicciones y configuración.
- Crear exactamente seis notebooks Colab independientes: `VGG16_Modelo_A_Train.ipynb`, `VGG16_Modelo_A_Test.ipynb`, `VGG16_Modelo_B_Train.ipynb`, `VGG16_Modelo_B_Test.ipynb`, `VGG16_Modelo_C_Train.ipynb` y `VGG16_Modelo_C_Test.ipynb`.
- Derivar cada notebook de los Colab `VGG16_Train.ipynb` y `VGG16_Test.ipynb` proporcionados por el profesor, conservando su orden y enfoque, y limitar los cambios a las líneas necesarias para dataset multiclase, cabezal neuronal, entrenamiento, métricas y artefactos.
- Evaluar cada modelo con matriz de confusión, Accuracy, Precision, Recall y F1 Score multiclase, incluyendo resultados por clase y promedios macro.
- Generar diagramas de arquitectura, gráficas de aprendizaje, histogramas/distribuciones y figuras comparativas.
- Elaborar un reporte en LaTeX que documente dataset, metodología, justificación de los cabezales, resultados, análisis y conclusión sobre el mejor modelo.
- Entregar los seis notebooks ejecutables, reporte y pesos entrenados en una estructura lista para comprimir y enviar.

## Capabilities

### New Capabilities

- `vgg16-experiment-pipeline`: Preparación reproducible de `tf_flowers`, definición y entrenamiento comparable de tres cabezales sobre una base VGG16 congelada, y persistencia de artefactos.
- `multiclass-model-evaluation`: Evaluación consistente de los tres modelos mediante matrices de confusión, Accuracy, Precision, Recall y F1 Score, junto con visualizaciones exportables.
- `latex-experiment-report`: Reporte académico reproducible en LaTeX con arquitecturas, gráficas, tablas, análisis y conclusión basada en evidencia.

### Modified Capabilities

Ninguna.

## Impact

- Se crearán seis notebooks Colab basados directamente en las dos plantillas proporcionadas; cualquier utilidad auxiliar será opcional y no sustituirá la ejecución autónoma de cada notebook.
- Se añadirán dependencias de Python para TensorFlow/Keras, TensorFlow Datasets, scikit-learn, NumPy, pandas, Matplotlib y Seaborn.
- Se generarán archivos `.keras` y/o `.weights.h5`, CSV/JSON de métricas e historiales, imágenes PNG/PDF y fuentes/compilado LaTeX.
- La ejecución objetivo será Google Colab; descargar el dataset y los pesos ImageNet requerirá acceso a Internet y el entrenamiento se beneficiará de GPU.
- Los artefactos binarios entrenados pueden ser grandes y deberán excluirse del control de versiones si exceden las políticas del repositorio, aunque sí se incluirán en el paquete final de entrega.
