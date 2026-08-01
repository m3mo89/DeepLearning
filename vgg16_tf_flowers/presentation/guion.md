# Guion de la presentación

Duración aproximada: **18 minutos 40 segundos**. Se priorizó mostrar de forma legible las arquitecturas, curvas y matrices de confusión de los tres modelos aunque el recorrido supere los 15 minutos.

## 1. Portada y objetivo — 0:40

**Propósito:** presentar el problema y la pregunta central.

**Qué decir:** En este proyecto comparé tres clasificadores para cinco tipos de flores. Los tres reutilizan VGG16; lo que cambia es la complejidad del cabezal. La pregunta es si agregar capas y parámetros produce una mejora real.

**Transición:** Primero conviene ver con qué datos trabajé.

## 2. El problema y los datos — 1:00

**Propósito:** dimensionar el conjunto y explicar la partición.

**Qué decir:** `tf_flowers` contiene 3,670 imágenes de dandelion, daisy, tulips, sunflowers y roses. Generé una partición estratificada 70/15/15 para entrenamiento, validación y prueba. La estratificación conserva aproximadamente la proporción de cada flor.

**Transición:** Como el conjunto no es enorme, en lugar de entrenar una red profunda desde cero utilicé transferencia de aprendizaje.

## 3. Transfer learning — 1:20

**Propósito:** explicar VGG16 congelada y el promedio global.

**Qué decir:** VGG16 parte de pesos aprendidos en ImageNet y aporta filtros para bordes, texturas y formas. Congelé sus capas para entrenar únicamente el clasificador. Su salida tiene forma 7×7×512. `GlobalAveragePooling2D` resume cada mapa y entrega 512 características. `Flatten` habría producido 25,088 entradas y millones de conexiones densas, con mayor costo y riesgo de sobreajuste.

**Transición:** Sobre esas mismas 512 características diseñé una comparación controlada.

## 4. Pregunta experimental A/B/C — 1:10

**Propósito:** justificar por qué se eligieron tres variantes.

**Qué decir:** A pregunta si las características ya son separables con una salida lineal. B agrega una transformación no lineal intermedia. C prueba mayor profundidad y añade `Dropout`. Datos, VGG16 y protocolo permanecen iguales; solo cambia el cabezal.

**Transición:** La diferencia de capacidad se aprecia claramente al contar sus parámetros.

## 5. Arquitecturas — 1:25

**Propósito:** comparar capas y complejidad.

**Qué decir:** A usa únicamente cinco salidas `softmax`, una por clase, y tiene 2,565 parámetros entrenables. B agrega 256 unidades ReLU y llega a 132,613. C utiliza 512 y 128 unidades con `Dropout`, alcanzando 328,965. `Dense` aprende combinaciones; `Dropout` no aprende pesos, sino que regulariza durante entrenamiento.

**Transición:** Ahora veamos cada arquitectura completa tal como aparece en el reporte.

## 6. Arquitectura del Modelo A — 0:40

**Propósito:** mostrar cómo se conecta el clasificador lineal con VGG16.

**Qué decir:** Los cinco bloques convolucionales de VGG16 permanecen congelados. Después del promedio global, A conecta directamente las 512 características con cinco neuronas `softmax`, una por clase. Es el cabezal mínimo del experimento.

**Transición:** B conserva toda esa base y añade una transformación intermedia.

## 7. Arquitectura del Modelo B — 0:40

**Propósito:** visualizar la capa oculta de 256 unidades.

**Qué decir:** B mantiene la misma entrada, los cinco bloques congelados y el promedio global. La diferencia es una capa `Dense` de 256 unidades ReLU antes de las cinco salidas. Esa capa aprende combinaciones no lineales de las características.

**Transición:** C amplía aún más el cabezal y agrega regularización.

## 8. Arquitectura del Modelo C — 0:40

**Propósito:** visualizar profundidad, `Dropout` y cuello de botella.

**Qué decir:** C agrega 512 unidades ReLU, `Dropout(0.5)` y después 128 unidades ReLU antes de clasificar. Es la variante con mayor capacidad; `Dropout` intenta reducir coadaptación durante entrenamiento.

**Transición:** Para comparar justamente estos tres cabezales, mantuve fijo el protocolo.

## 9. Protocolo y semilla — 1:10

**Propósito:** demostrar comparabilidad y reproducibilidad.

**Qué decir:** Los tres usan Adam, lotes de 16, hasta 30 épocas, aumentación y `EarlyStopping`. La semilla 42 controla la partición y varias operaciones aleatorias para hacer la comparación más justa. No mejora el modelo ni elimina toda variación entre hardware.

**Transición:** Con el entrenamiento controlado, faltaba definir cómo decidir cuál funcionó mejor.

## 10. Métricas y sobreajuste — 1:15

**Propósito:** justificar F1 macro y explicar generalización.

**Qué decir:** Además de Accuracy medí Precision, Recall y F1 por clase. Elegí F1 macro como criterio principal porque asigna el mismo peso a las cinco flores. También observé la brecha entre entrenamiento, validación y prueba: cuando entrenamiento mejora pero validación empeora, aparece un indicio de sobreajuste.

**Transición:** Con esa regla, estos fueron los resultados.

## 11. Comparación global — 1:30

**Propósito:** comunicar el hallazgo principal.

**Qué decir:** A obtuvo F1 macro de 0.8799 y Accuracy de 0.8802. B quedó muy cerca, con F1 de 0.8775; C obtuvo 0.8652. A también tuvo la menor brecha y muchos menos parámetros. Por eso fue seleccionado. La ventaja sobre B es pequeña, así que no afirmo una superioridad universal.

**Transición:** El promedio global no muestra en qué clases se producen los errores; la matriz sí.

## 12. Curvas del Modelo A — 0:50

**Propósito:** revisar la dinámica de entrenamiento del ganador.

**Qué decir:** A la izquierda aparece la pérdida, donde un valor menor es mejor; a la derecha está Accuracy, donde un valor mayor es mejor. Azul representa entrenamiento y naranja validación. A conservó su mejor checkpoint en la época 14. La separación entre curvas ayuda a valorar si el aprendizaje se mantiene en datos no usados para actualizar los pesos.

**Transición:** B tiene muchas más conexiones; revisemos si eso cambia la dinámica.

## 13. Curvas del Modelo B — 0:50

**Propósito:** observar la variante de capacidad intermedia.

**Qué decir:** B conservó su mejor checkpoint en la época 9. Aunque aprende una transformación no lineal adicional, su resultado de prueba queda apenas por debajo de A y su brecha de generalización es mayor.

**Transición:** C añade todavía más capacidad y `Dropout`.

## 14. Curvas del Modelo C — 0:50

**Propósito:** observar el efecto del cabezal profundo regularizado.

**Qué decir:** C conserva su mejor checkpoint en la época 6. `Dropout` intenta reducir coadaptación, pero las curvas y la evaluación final muestran que regularizar no garantiza que la capacidad adicional produzca mejor generalización.

**Transición:** Después de revisar cómo aprendieron, veamos en qué clases se equivocó cada uno.

## 15. Análisis del Modelo A — 1:20

**Propósito:** interpretar errores y desempeño por clase.

**Qué decir:** En las matrices, las filas son clases reales y las columnas predicciones. La diagonal contiene aciertos y las celdas externas muestran confusiones. La matriz izquierda presenta cantidades; la derecha proporciones por clase. `sunflowers` alcanzó el mejor F1, 0.9048, mientras `roses` obtuvo 0.8317.

**Transición:** Para comprobar si ese patrón cambia con mayor capacidad, revisemos B y C.

## 16. Matriz del Modelo B — 0:50

**Propósito:** mostrar los errores de la variante intermedia.

**Qué decir:** B obtiene un resultado muy cercano a A, pero requiere 132,613 parámetros entrenables. Su matriz conserva confusiones entre clases visualmente parecidas y su brecha validación--prueba aumenta a 0.0308.

**Transición:** C lleva todavía más lejos la capacidad del cabezal e incorpora regularización.

## 17. Matriz del Modelo C — 0:50

**Propósito:** mostrar que mayor profundidad y `Dropout` no garantizaron una mejora.

**Qué decir:** C alcanza F1 macro de 0.8652 y la mayor brecha, 0.0367. `Dropout` reduce riesgo de coadaptación, pero no crea información nueva ni asegura que un modelo grande generalice mejor.

**Transición:** Con las curvas y matrices de los tres modelos, ya podemos cerrar la comparación.

## 18. Conclusiones y limitaciones — 1:20

**Propósito:** cerrar el argumento sin exagerar los resultados.

**Qué decir:** VGG16 congelada ya produjo características útiles y el cabezal mínimo ofreció el mejor equilibrio. Más capas dieron mayor capacidad, pero no información nueva. El estudio tiene 3,670 imágenes, una sola semilla y no incluye búsqueda exhaustiva ni `fine-tuning`; repetir con varias semillas sería el siguiente paso.

**Transición:** En resumen, más complejo no siempre significa mejor. Gracias; con gusto respondo preguntas.

## 19. Preguntas — 0:20

**Propósito:** abrir la discusión con un cierre visual ligero.

**Qué decir:** El meme resume el hallazgo principal: esperábamos que más capas ayudaran, pero el Modelo A fue suficiente en esta ejecución. ¿Preguntas?

## Resumen temporal

| Diapositiva | Tiempo |
|---|---:|
| 1. Portada | 0:40 |
| 2. Datos | 1:00 |
| 3. Transfer learning | 1:20 |
| 4. Pregunta A/B/C | 1:10 |
| 5. Arquitecturas | 1:25 |
| 6. Arquitectura A | 0:40 |
| 7. Arquitectura B | 0:40 |
| 8. Arquitectura C | 0:40 |
| 9. Protocolo | 1:10 |
| 10. Métricas | 1:15 |
| 11. Resultados | 1:30 |
| 12. Curvas A | 0:50 |
| 13. Curvas B | 0:50 |
| 14. Curvas C | 0:50 |
| 15. Matriz A | 1:20 |
| 16. Matriz B | 0:50 |
| 17. Matriz C | 0:50 |
| 18. Conclusiones | 1:20 |
| 19. Preguntas | 0:20 |
| **Total** | **18:40** |
