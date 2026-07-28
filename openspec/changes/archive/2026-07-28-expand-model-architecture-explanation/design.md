## Context

El reporte actual ya documenta las tres arquitecturas y sus conteos de parámetros, pero introduce `Dense`, ReLU, `softmax` y `Dropout` directamente dentro de cada modelo. Para un lector que aún no domina redes neuronales, esto dificulta distinguir entre el número de neuronas, la activación aplicada, la función de cada capa y el carácter independiente de los experimentos.

Las arquitecturas no deben cambiar:

- A: vector de 512 características → `Dense(5, softmax)`.
- B: vector de 512 características → `Dense(256, relu)` → `Dense(5, softmax)`.
- C: vector de 512 características → `Dense(512, relu)` → `Dropout(0.5)` → `Dense(128, relu)` → `Dense(5, softmax)`.

Los tres modelos reutilizan una instancia conceptualmente equivalente de VGG16 con pesos de ImageNet congelados. Cada ejecución construye e inicializa aleatoriamente su propio cabezal y lo entrena de manera independiente con los mismos datos y configuración para que la comparación sea válida.

## Goals / Non-Goals

**Goals:**

- Dar al lector definiciones suficientes de `Dense`, ReLU, `softmax` y `Dropout` antes de depender de esos términos.
- Relacionar las dimensiones 5, 256, 512 y 128, y la tasa 0.5, con decisiones concretas del experimento.
- Explicar por qué cada cantidad de neuronas fue elegida frente a alternativas razonables, sin confundir una hipótesis experimental con un valor óptimo.
- Explicar el flujo de información y el efecto de cada componente en A, B y C.
- Diferenciar con precisión la reutilización del backbone preentrenado de la inicialización independiente de cada cabezal.
- Mantener una narrativa gradual: conceptos comunes, Modelo A como línea base, B como variante de capacidad intermedia y C como variante más profunda regularizada.
- Enseñar a interpretar curvas de aprendizaje, matrices de confusión, métricas por clase e histogramas de confianza.
- Vincular la selección de A con la regla previa, las métricas de prueba, la brecha de generalización y la complejidad.

**Non-Goals:**

- Cambiar las arquitecturas, hiperparámetros, datos, notebooks o resultados.
- Afirmar que 256, 512, 128 o 0.5 son valores universalmente óptimos; se presentarán como hipótesis de diseño que el experimento compara.
- Reemplazar el análisis de resultados con teoría general de redes neuronales.
- Introducir derivaciones matemáticas extensas que desplacen el propósito aplicado del reporte.

## Decisions

### 1. Añadir una base conceptual común antes de los modelos

Se incorporará una subsección breve antes de “Modelos propuestos” que defina:

- Una capa `Dense` como una transformación afín \(z=Wx+b\), donde cada neurona recibe todas las entradas; el número de unidades determina el tamaño del vector producido y afecta directamente el número de parámetros.
- Una activación como la función aplicada a \(z\), dejando claro que `Dense(256, activation="relu")` combina la transformación densa y ReLU en una sola declaración.
- ReLU como \(\max(0,z)\), que introduce no linealidad, conserva valores positivos y anula valores negativos.
- `softmax` como la normalización de cinco logits a probabilidades no negativas cuya suma es uno, adecuada para una sola etiqueta entre cinco clases.
- `Dropout(0.5)` como una técnica usada únicamente durante entrenamiento que anula aleatoriamente la mitad de activaciones y ajusta la escala, sin añadir parámetros entrenables.

Alternativa considerada: repetir definiciones completas en cada modelo. Se descarta porque aumenta redundancia; cada subsección reutilizará las definiciones comunes y se concentrará en su efecto particular.

### 2. Separar “cantidad de clases” de “capacidad oculta”

El reporte explicará que las cinco unidades de la última capa están determinadas por las cinco categorías del conjunto de datos, mientras que 256, 512 y 128 son hiperparámetros de capas ocultas. Por ello B y C conservan una salida de cinco unidades aunque tengan mayor capacidad interna.

Alternativa considerada: describir todos los números simplemente como “cantidad de neuronas”. Se descarta porque oculta que la dimensión de salida está fijada por el problema, mientras las dimensiones ocultas son decisiones experimentales.

### 3. Presentar las variantes como comparables, no encadenadas

Se afirmará explícitamente:

- A, B y C comparten el diseño del extractor VGG16 y parten de los mismos pesos preentrenados de ImageNet.
- VGG16 permanece congelado en cada modelo.
- Los pesos del cabezal de cada variante se inicializan y optimizan por separado.
- B toma a A como referencia experimental para agregar capacidad, pero no carga ni continúa los pesos aprendidos por A.
- C toma a A y B como referencias de diseño, pero tampoco carga ni continúa sus pesos.

Esta formulación evita los dos extremos incorrectos: decir que cada modelo parte totalmente desde cero ignoraría ImageNet; decir que B deriva del entrenamiento de A o C del de B implicaría una herencia de pesos que no existe.

### 4. Justificar las capas como hipótesis experimentales

- En A, cinco neuronas no son una elección ajustable entre 4, 5 o 10: existe una por cada clase. `Dense(5, softmax)` será la arquitectura mínima compatible con el problema y probará si las 512 características de VGG16 ya son linealmente separables.
- En B, 256 unidades serán una elección intermedia y deliberadamente menor que las 512 características de entrada. Frente a 64 o 128 ofrecen más combinaciones; frente a 512 o 1024 limitan parámetros y riesgo de memorización. ReLU permitirá fronteras no lineales a costa de elevar los parámetros de 2,565 a 132,613.
- En C, 512 unidades igualarán la dimensión del vector recibido para explorar una representación amplia sin expansión dimensional inicial; elegir 1024 duplicaría aproximadamente el costo de esa primera capa. Las 128 unidades posteriores reducirán la representación a una cuarta parte y actuarán como cuello de botella; frente a conservar 512, disminuyen parámetros y fuerzan una síntesis, y frente a 32 o 64 evitan una compresión demasiado abrupta. `Dropout(0.5)` responderá al mayor riesgo de sobreajuste; el total será 328,965 parámetros.

Los valores se describirán como elecciones razonadas para comparar niveles de capacidad, no como resultado de una búsqueda exhaustiva ni como garantías de mejora. La evidencia final seguirá siendo el desempeño medido, que en este experimento favoreció al modelo A.

### 5. Mantener consistencia terminológica y tipográfica

Se usará “neuronas” o “unidades” para dimensiones, “capa densa” para `Dense`, “activación” para ReLU y `softmax`, y “cabezal clasificador” para la parte entrenable posterior a VGG16. Se corregirán términos y redacción sin alterar nombres literales de API.

### 6. Explicar cómo leer cada visualización

La sección de métricas introducirá una guía de lectura que después se aplicará a cada figura:

- Las curvas de pérdida muestran el error optimizado y las de exactitud el porcentaje de aciertos por época. Entrenamiento y validación mejorando juntas sugieren aprendizaje; entrenamiento mejorando mientras validación se estanca o empeora sugiere sobreajuste; ambas con desempeño bajo sugieren subajuste.
- En la matriz de confusión, las filas serán clases reales y las columnas clases predichas. La diagonal serán aciertos; las celdas fuera de ella mostrarán qué clases se confunden. La matriz absoluta permitirá contar casos y la normalizada comparar proporciones aunque los soportes difieran.
- Las barras por clase separarán Precision, Recall y F1. Precision responderá “de todo lo predicho como esta clase, cuánto fue correcto”; Recall, “de todos los ejemplos reales de esta clase, cuántos recuperó”; F1 equilibrará ambas.
- El histograma usará como confianza el máximo de las cinco probabilidades `softmax`. Separará aciertos y errores para mostrar si los errores se concentran en baja confianza o si existen errores de alta confianza. Confianza no equivale a certeza ni demuestra calibración.
- La comparación global combinará Accuracy, F1 macro, brecha validación–prueba y parámetros entrenables, evitando escoger un modelo por una sola imagen o clase.

### 7. Explicar la victoria de A como resultado empírico

La discusión seguirá la regla fijada antes del experimento: mayor F1 macro de prueba, luego Accuracy, menor brecha de generalización y menor complejidad. Incorporará estos valores:

- A: F1 macro 0.8799, Accuracy 0.8802, brecha 0.0219 y 2,565 parámetros entrenables.
- B: F1 macro 0.8775, Accuracy 0.8784, brecha 0.0308 y 132,613 parámetros entrenables.
- C: F1 macro 0.8652, Accuracy 0.8675, brecha 0.0367 y 328,965 parámetros entrenables.

Las capas adicionales aumentan la capacidad para representar funciones complejas, pero no incorporan automáticamente información nueva. Como VGG16 ya entrega características útiles y el conjunto tiene 3,670 imágenes, A pudo encontrar una frontera suficiente con menor varianza. B y C tuvieron más libertad para ajustarse a particularidades del entrenamiento; Dropout redujo ese riesgo en C, pero no garantiza superar una solución sencilla.

La diferencia entre A y B se calificará como pequeña. A es el ganador conforme a la regla definida y a esta ejecución, pero no se afirmará significancia estadística porque no hubo múltiples semillas ni intervalos de confianza.

## Risks / Trade-offs

- [La explicación puede volverse demasiado extensa] → Usar una base conceptual común y reservar en cada modelo solo el efecto específico de sus capas.
- [El lector puede interpretar 256, 512, 128 y 0.5 como valores óptimos] → Etiquetarlos como hiperparámetros elegidos para comparar niveles de capacidad y regularización.
- [“Parte desde cero” puede seguir siendo ambiguo] → Distinguir explícitamente pesos congelados de ImageNet y pesos nuevos del cabezal.
- [Una simplificación de Dropout puede ser técnicamente imprecisa en inferencia] → Indicar que el descarte ocurre durante entrenamiento y que en evaluación se usa la red completa con el escalado correspondiente.
- [La edición puede introducir discrepancias con fórmulas o resultados] → Verificar arquitectura, conteos de parámetros y compilación del reporte después de editar.
- [Una gráfica puede sobreinterpretarse como prueba causal] → Separar observación, interpretación e hipótesis, y no afirmar significancia estadística sin repeticiones.
- [La confianza Softmax puede confundirse con certeza real] → Definirla como el máximo Softmax y advertir que puede estar mal calibrada, incluso en errores.
