## 1. Estructura y estilo Beamer

- [x] 1.1 Crear `vgg16_tf_flowers/presentation/` y el fuente Beamer panorámico con metadatos de autor, paleta sobria, tipografía legible y rutas reutilizables hacia las figuras.
- [x] 1.2 Implementar la portada, diez diapositivas de contenido y una diapositiva final de preguntas conforme a la narrativa y tiempos definidos.
- [x] 1.3 Integrar en la diapositiva de preguntas un meme original y discreto sobre CNN o VGG16 como activo local, sin recursos externos de atribución incierta.

## 2. Contenido académico y evidencia

- [x] 2.1 Integrar dataset, partición, VGG16 congelada y `GlobalAveragePooling2D` con visualizaciones legibles y explicación concisa.
- [x] 2.2 Presentar la lógica experimental, arquitecturas y parámetros de A, B y C manteniendo claro qué cambió y qué permaneció fijo.
- [x] 2.3 Resumir protocolo, semilla, F1 macro, generalización y sobreajuste sin trasladar explicaciones extensas del reporte.
- [x] 2.4 Incorporar la comparación de resultados y el análisis del Modelo A con cifras y figuras trazables a los artefactos existentes.
- [x] 2.5 Cerrar con conclusión, limitaciones y trabajo futuro, aclarando que una sola ejecución no demuestra superioridad universal ni significancia estadística.
- [x] 2.6 Presentar en diapositivas separadas y legibles las curvas de aprendizaje de A, B y C.
- [x] 2.7 Añadir diapositivas legibles para las matrices de confusión de B y C, conservando la diapositiva existente de A.
- [x] 2.8 Añadir descripciones breves para interpretar ejes, líneas, diagonal, celdas externas y normalización de las curvas y matrices.
- [x] 2.9 Añadir diapositivas separadas con las imágenes completas de arquitectura de A, B y C utilizadas en el reporte.

## 3. Guion y documentación

- [x] 3.1 Actualizar `presentation/guion.md` con las nuevas arquitecturas, explicación oral y un total aproximado de 18–19 minutos.
- [x] 3.2 Añadir al README la ubicación del fuente, PDF y guion, junto con el comando de compilación Tectonic.

## 4. Compilación y validación

- [x] 4.1 Recompilar `presentacion.tex`, resolver referencias, codificación, recursos faltantes y desbordamientos, y conservar `presentacion.pdf`.
- [x] 4.2 Revisar visualmente las diecinueve diapositivas a escala de presentación y corregir texto pequeño, saturación, recortes o contraste insuficiente.
- [x] 4.3 Verificar dieciocho diapositivas de contenido, la diapositiva final de preguntas, la suma de tiempos, métricas, parámetros, clases, selección del ganador y ausencia de afirmaciones no respaldadas.
- [x] 4.4 Ejecutar nuevamente la validación de entrega y comprobar que la ampliación no altera notebooks, pesos, métricas ni resultados.
