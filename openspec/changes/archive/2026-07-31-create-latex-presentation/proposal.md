## Why

La entrega necesita una presentación oral que sintetice el experimento VGG16 y muestre evidencia suficiente de los tres modelos, sin convertir el reporte completo en diapositivas saturadas. Una presentación Beamer reproducible permitirá comunicar el objetivo, las decisiones metodológicas, las curvas, matrices, resultados reales y sus limitaciones con una narrativa visual coherente con la documentación académica existente.

## What Changes

- Crear una presentación en LaTeX Beamer dentro del proyecto, con fuente editable y PDF compilado.
- Organizar dieciocho diapositivas de contenido y una diapositiva final de preguntas para una exposición aproximada de 18–19 minutos.
- Cubrir portada, objetivo, dataset, transferencia con VGG16, lógica de A/B/C, arquitecturas, protocolo, métricas, resultados, análisis del ganador, conclusiones y limitaciones.
- Reutilizar las figuras reales del dataset, arquitecturas, comparación y evaluación ya generadas por el experimento.
- Mostrar las curvas de aprendizaje de A, B y C y las matrices de confusión de los tres modelos dentro del recorrido principal.
- Mostrar las imágenes completas de las arquitecturas A, B y C utilizadas en el reporte.
- Incluir notas breves de exposición o una guía temporal que indique el mensaje principal y tiempo aproximado de cada diapositiva.
- Cerrar con una diapositiva de preguntas que incluya un meme original y discreto relacionado con CNN o VGG16, sin depender de recursos externos con atribución incierta.
- Mantener una densidad visual apropiada: ideas clave, cifras esenciales y gráficos legibles, dejando los detalles secundarios como material de respaldo si resultan necesarios.
- Conservar la trazabilidad de todas las métricas y afirmaciones con los JSON, CSV, figuras y reporte existentes.
- Documentar en el README cómo compilar y localizar la presentación.

## Capabilities

### New Capabilities

- `latex-academic-presentation`: presentación académica Beamer reproducible, visualmente legible, basada en resultados reales y ajustada a una exposición de máximo 15 minutos.

### Modified Capabilities

Ninguna.

## Impact

Se añadirá un directorio de presentación bajo `vgg16_tf_flowers/`, con fuente `.tex`, PDF y, si se requiere, un archivo de notas. Se reutilizarán recursos de `vgg16_tf_flowers/figures/` y datos de `results/` y `report/`; no se modificarán notebooks, modelos, pesos, métricas ni el reporte académico. El README recibirá instrucciones breves de compilación.
