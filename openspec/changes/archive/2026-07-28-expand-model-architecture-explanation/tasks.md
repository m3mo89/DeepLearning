## 1. Fundamentos conceptuales

- [x] 1.1 Añadir en `vgg16_tf_flowers/report/main.tex`, antes de los modelos propuestos, una explicación de capa `Dense`, transformación \(Wx+b\), unidades, pesos, sesgos y efecto sobre la cantidad de parámetros.
- [x] 1.2 Explicar ReLU, `softmax` y `Dropout`, distinguiendo capa, activación y regularización, e indicando el comportamiento diferente de Dropout durante entrenamiento e inferencia.
- [x] 1.3 Explicar que cinco unidades de salida corresponden a las cinco clases mutuamente excluyentes y que `softmax` convierte logits en probabilidades que suman uno.

## 2. Explicación de los modelos

- [x] 2.1 Ampliar el Modelo A para describir el flujo de 512 características a cinco clases, justificar `Dense(5, softmax)`, explicar su efecto como clasificador lineal y conservar el conteo de 2,565 parámetros.
- [x] 2.2 Ampliar el Modelo B para explicar `Dense(256) + ReLU`, justificar 256 como capacidad intermedia, describir el aumento a 132,613 parámetros y aclarar por qué la salida permanece en cinco neuronas `softmax`.
- [x] 2.3 Ampliar el Modelo C para explicar `Dense(512) + ReLU`, justificar `Dropout(0.5)`, describir `Dense(128) + ReLU` como cuello de botella, explicar la salida de cinco clases y conservar el conteo de 328,965 parámetros.
- [x] 2.4 Añadir una aclaración explícita de que B se inspira en A y C compara mayor capacidad frente a A y B, pero los tres cabezales se inicializan y entrenan de forma independiente sobre copias equivalentes del mismo VGG16 congelado con pesos de ImageNet.
- [x] 2.5 Contrastar 256, 512 y 128 con alternativas menores y mayores, dejando claro que son hiperparámetros razonados y no valores óptimos obtenidos mediante búsqueda exhaustiva.

## 3. Lectura de resultados

- [x] 3.1 Ampliar la sección de métricas para enseñar a leer Accuracy, Precision, Recall, F1, soporte y promedios macro y ponderado, conectándolos con TP, TN, FP y FN.
- [x] 3.2 Explicar las curvas de pérdida y exactitud de entrenamiento y validación, incluidos convergencia, sobreajuste, subajuste y brecha de generalización.
- [x] 3.3 Explicar los ejes, diagonal y celdas externas de las matrices de confusión absoluta y normalizada, y aplicar la lectura a las confusiones observadas.
- [x] 3.4 Explicar las barras de métricas por clase y cómo una diferencia entre Precision y Recall revela tipos distintos de error.
- [x] 3.5 Explicar que el histograma usa el máximo Softmax como confianza, cómo comparar aciertos y errores y por qué alta confianza no garantiza corrección ni calibración.
- [x] 3.6 Ampliar leyendas o texto adyacente para que cada figura indique qué representa, qué patrón observar y qué conclusión puede extraerse.

## 4. Selección del ganador

- [x] 4.1 Comparar A, B y C usando F1 macro, Accuracy, brecha validación–prueba y parámetros entrenables, con los valores generados.
- [x] 4.2 Explicar por qué mayor profundidad y número de parámetros incrementan capacidad pero no garantizan mejor rendimiento ni generalización.
- [x] 4.3 Relacionar la victoria de A con las características preentrenadas de VGG16, el tamaño del conjunto, la menor complejidad y la regla de selección previa.
- [x] 4.4 Señalar que la ventaja de A sobre B es pequeña y que no se puede afirmar significancia estadística sin múltiples semillas o intervalos de confianza.

## 5. Consistencia y validación

- [x] 5.1 Revisar que los valores, fórmulas, términos y afirmaciones coincidan con configuración, notebooks, matrices, historiales, predicciones, métricas y resúmenes.
- [x] 5.2 Confirmar que la ampliación no modifica arquitecturas, código de entrenamiento, métricas ni la conclusión que selecciona al Modelo A.
- [x] 5.3 Compilar el reporte LaTeX y corregir errores de composición, referencias, desbordamientos o legibilidad introducidos por el texto nuevo.
- [x] 5.4 Inspeccionar el PDF resultante para comprobar el orden pedagógico y la cobertura de los requisitos de arquitectura y evaluación.
