## 1. Integración pedagógica del reporte

- [x] 1.1 Revisar el flujo y preámbulo de `vgg16_tf_flowers/report/main.tex` para ubicar las nuevas explicaciones sin duplicar contenido y confirmar soporte para la tabla comparativa.
- [x] 1.2 Ampliar la explicación de la semilla 42 con fuentes de aleatoriedad controladas, propósito comparativo, no determinismo residual y limitación de una sola ejecución.
- [x] 1.3 Incorporar una definición de sobreajuste, subajuste y brecha de generalización, conectándola con las curvas y mitigaciones ya utilizadas.

## 2. Justificación de arquitectura y alcance

- [x] 2.1 Añadir el contraste entre `GlobalAveragePooling2D` y `Flatten`, verificando las dimensiones y conteos hipotéticos de parámetros de A, B y C.
- [x] 2.2 Introducir la lógica conjunta de A, B y C como comparación controlada de capacidad mínima, intermedia y profunda regularizada.
- [x] 2.3 Afinar las definiciones de `Dense` y `Dropout` para distinguir transformación de características y regularización sin alterar las explicaciones correctas existentes.
- [x] 2.4 Añadir la tabla de alternativas no evaluadas con función, ventaja potencial y motivo de exclusión, separando opciones arquitectónicas de técnicas de regularización.
- [x] 2.5 Explicar que las alternativas quedaron fuera del alcance para aislar variables y limitar la búsqueda combinatoria, sin afirmar que sean inferiores.

## 3. Verificación y entrega

- [x] 3.1 Comprobar que arquitecturas, parámetros implementados, configuración, métricas, figuras, resultados y selección del Modelo A permanezcan sin cambios.
- [x] 3.2 Compilar el reporte LaTeX, corregir desbordamientos o referencias y regenerar los PDF de entrega.
- [x] 3.3 Ejecutar la validación de entrega y revisar que no existan marcadores pendientes ni afirmaciones que presenten alternativas como evaluadas.
