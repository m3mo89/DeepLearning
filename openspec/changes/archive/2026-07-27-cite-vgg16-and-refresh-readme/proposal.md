## Why

El reporte incluye la referencia fundacional de VGG16 de Simonyan y Zisserman, pero no la cita en el cuerpo, por lo que actualmente aparece como una entrada bibliográfica huérfana. Además, el único README del repositorio está dentro de `vgg16_tf_flowers/` y describe el flujo principal, pero puede aclarar prerrequisitos, directorio de ejecución, ruta esperada en Google Drive y alternativas para compilar el reporte.

## What Changes

- Añadir una cita `\cite{vgg}` en el pasaje del reporte que introduce VGG16 preentrenada y explica su papel como extractor de características.
- Verificar que las dos entradas bibliográficas del reporte sean utilizadas y que la compilación no produzca citas indefinidas.
- Revisar `vgg16_tf_flowers/README.md` contra la estructura, los notebooks y los scripts actuales.
- Aclarar que los comandos locales se ejecutan desde la raíz `vgg16_tf_flowers/`.
- Documentar la instalación local mediante `requirements.txt` sin convertirla en requisito para el flujo de Google Colab.
- Hacer explícita la ruta de Drive esperada por los notebooks (`/content/drive/MyDrive/vgg16_tf_flowers`) y cómo proceder si se usa otro nombre o ubicación.
- Documentar tanto `pdflatex` como Tectonic para compilar `report/main.tex`, indicando el nombre esperado `reporte_vgg16.pdf`.
- Mantener actualizadas las instrucciones de validación, empaquetado y ubicación del ZIP resultante.

## Capabilities

### New Capabilities

- `academic-citation-and-readme-guidance`: Requisitos para que las referencias académicas del reporte estén citadas y el README describa de forma verificable los flujos de instalación, ejecución, compilación, validación y empaquetado.

### Modified Capabilities

Ninguna.

## Impact

- Archivos previstos: `vgg16_tf_flowers/report/main.tex` y `vgg16_tf_flowers/README.md`.
- Se regenerarán `vgg16_tf_flowers/report/main.pdf` y `vgg16_tf_flowers/report/reporte_vgg16.pdf` para validar y conservar el reporte compilado.
- No cambian modelos, notebooks, resultados, pesos, métricas, dependencias fijadas ni scripts.
