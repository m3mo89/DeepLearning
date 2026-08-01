## Context

El proyecto ya contiene un reporte académico compilado, resultados completos y figuras suficientes para explicar el experimento. La nueva necesidad no es reproducir el reporte página por página, sino convertirlo en una exposición oral de máximo 15 minutos. El público debe poder seguir el problema, la comparación controlada y la conclusión sin leer párrafos extensos ni descifrar tablas densas.

La presentación debe identificarse como trabajo de Guillermo Tinoco Ramos, mantener las cifras reales —3,670 imágenes; cinco clases; F1 macro A=0.8799, B=0.8775 y C=0.8652— y conservar la conclusión matizada: A gana bajo la regla y ejecución definidas, pero su diferencia con B es pequeña y no establece superioridad universal.

## Goals / Non-Goals

**Goals:**

- Producir una presentación Beamer en formato panorámico 16:9 y su PDF compilado.
- Sostener una narrativa de dieciocho diapositivas de contenido, una diapositiva final de preguntas y aproximadamente 18–19 minutos ensayados.
- Priorizar visualizaciones, comparaciones directas y una idea principal por diapositiva.
- Explicar suficientemente VGG16, `GlobalAveragePooling2D`, A/B/C, semilla, métricas y sobreajuste sin convertir la exposición en una clase teórica extensa.
- Mostrar resultados, análisis por clase, limitaciones y posibles extensiones con trazabilidad a los artefactos existentes.
- Incluir un guion breve con tiempos y transiciones para facilitar el ensayo.

**Non-Goals:**

- Presentar todas las fórmulas, alternativas o figuras incluidas en el reporte.
- Añadir resultados nuevos, volver a entrenar modelos o modificar el experimento.
- Afirmar significancia estadística o superioridad general de A.
- Crear una presentación interactiva, animaciones complejas o dependencias ajenas a LaTeX.

## Decisions

### Usar Beamer 16:9 con un estilo académico sobrio

El fuente principal será `vgg16_tf_flowers/presentation/presentacion.tex`, basado en `beamer` con relación `aspectratio=169`. Se preferirá una paleta coherente, alto contraste, tipografía grande y navegación visual mínima. Beamer permite mantener la presentación como código reproducible y compilarla con Tectonic, ya utilizado en el reporte.

Se descarta duplicar el estilo `article` del reporte porque no está optimizado para proyección, y se evita una plantilla visual recargada porque competiría con las gráficas.

### Mantener diez diapositivas principales

El recorrido previsto será:

1. Portada y objetivo.
2. Dataset y partición.
3. Transfer learning con VGG16 y elección del promedio global.
4. Pregunta experimental y lógica A/B/C.
5. Arquitecturas y parámetros entrenables.
6. Arquitectura visual completa del Modelo A.
7. Arquitectura visual completa del Modelo B.
8. Arquitectura visual completa del Modelo C.
9. Protocolo reproducible y semilla.
10. Métricas, F1 macro y sobreajuste.
11. Comparación de resultados.
12. Curvas de aprendizaje del Modelo A.
13. Curvas de aprendizaje del Modelo B.
14. Curvas de aprendizaje del Modelo C.
15. Matriz de confusión y análisis del Modelo A.
16. Matriz de confusión del Modelo B.
17. Matriz de confusión del Modelo C.
18. Conclusiones, limitaciones y trabajo futuro.
19. Preguntas, con un cierre visual ligero relacionado con CNN o VGG16.

El tiempo objetivo suma aproximadamente 18 minutos 40 segundos. La diapositiva de preguntas utilizará aproximadamente 20–30 segundos como transición hacia la discusión, sin añadir contenido técnico nuevo. Las arquitecturas, curvas y matrices de los tres modelos forman parte del recorrido principal porque se priorizó mostrar evidencia legible y completa sobre conservar el límite original de 15 minutos.

### Cerrar con preguntas y un meme original

La última diapositiva mostrará el título ``Preguntas'', un agradecimiento breve y un meme original sobre CNN o VGG16 integrado como activo local de la presentación. El humor será académico y discreto —por ejemplo, contrastar ``agregar más capas'' con el resultado favorable del modelo sencillo— y no ridiculizará personas, clases o resultados. Se evita descargar un meme existente para no introducir problemas de licencia, atribución o calidad visual.

### Reutilizar figuras y simplificar tablas

Se usarán prioritariamente `mosaico_dataset.png`, `histograma_clases_splits.png`, las arquitecturas visuales, `comparacion_modelos.png` y la matriz o métricas por clase de A. Las figuras se referenciarán desde `../figures/` para no duplicar activos.

Las tablas se reducirán a cifras necesarias para la exposición: Accuracy, F1 macro y parámetros entrenables. No se trasladarán tablas completas de Precision/Recall, tiempos o alternativas no evaluadas salvo como respaldo.

### Separar contenido visible y guion oral

Cada diapositiva mostrará frases cortas y cifras, mientras un archivo `guion.md` registrará propósito, tiempo aproximado, explicación oral y transición. Esto evita saturar la proyección y permite comprobar el límite temporal. El guion será una ayuda, no un texto para leer literalmente.

### Mantener afirmaciones trazables y prudentes

Las cifras se contrastarán con `results/comparacion_modelos.csv`, métricas por clase y el reporte. La presentación indicará que A obtuvo el mejor resultado de esta ejecución, que la ventaja sobre B es pequeña y que múltiples semillas serían necesarias para estudiar estabilidad o significancia.

## Risks / Trade-offs

- [La presentación puede superar el límite original de 15 minutos] → Documentar un guion aproximado de 15–16 minutos y priorizar la evidencia de los tres modelos según la nueva decisión del usuario.
- [Las figuras del reporte pueden tener texto pequeño al proyectarse] → Seleccionar recortes o escalas legibles y revisar visualmente el PDF a tamaño de presentación.
- [Demasiados conceptos pueden saturar la exposición] → Mantener una idea principal por diapositiva y mover detalles a respaldo o al guion.
- [El PDF puede reproducir problemas de codificación] → Usar formas LaTeX seguras para signos iniciales y verificar texto extraído, como se hizo con el reporte.
- [Las cifras pueden divergir del reporte] → Comparar automáticamente o manualmente cada valor mostrado contra los resultados exportados.
- [Beamer puede requerir paquetes no almacenados localmente] → Compilar con Tectonic y documentar el comando; no introducir paquetes decorativos innecesarios.
- [El meme puede restar seriedad o consumir tiempo] → Usar humor breve, original y relacionado con la conclusión; reservarlo exclusivamente para la diapositiva final de preguntas.
