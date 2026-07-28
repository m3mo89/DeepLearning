## 1. Cita académica

- [x] 1.1 Añadir `\cite{vgg}` a la primera introducción metodológica de VGG16 en `vgg16_tf_flowers/report/main.tex`.
- [x] 1.2 Verificar que cada clave declarada con `\bibitem` sea utilizada en el cuerpo del reporte.
- [x] 1.3 Compilar el reporte y confirmar que no existan citas o referencias indefinidas.

## 2. Revisión del README

- [x] 2.1 Añadir una sección breve de prerrequisitos y preparación local con Python 3, `requirements.txt` y un compilador LaTeX.
- [x] 2.2 Aclarar que los comandos de scripts se ejecutan desde la raíz `vgg16_tf_flowers/`.
- [x] 2.3 Documentar que los notebooks esperan `/content/drive/MyDrive/vgg16_tf_flowers` y qué celdas de ruta adaptar si cambia la ubicación.
- [x] 2.4 Mantener el flujo `pdflatex` y añadir una alternativa Tectonic que termine produciendo `report/reporte_vgg16.pdf`.
- [x] 2.5 Aclarar la diferencia entre validación estructural y estricta, y que el ZIP final se crea en el directorio padre.
- [x] 2.6 Contrastar todos los archivos, comandos, opciones y salidas mencionados en el README con la implementación actual.

## 3. Artefactos y validación final

- [x] 3.1 Regenerar `report/main.pdf` y `report/reporte_vgg16.pdf` a partir del reporte citado.
- [x] 3.2 Ejecutar la validación estructural y estricta del entregable.
- [x] 3.3 Revisar el diff para confirmar que no cambiaron notebooks, modelos, resultados, pesos ni dependencias.
