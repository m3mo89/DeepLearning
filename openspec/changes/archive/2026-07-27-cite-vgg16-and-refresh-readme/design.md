## Context

`vgg16_tf_flowers/report/main.tex` presenta VGG16 como backbone preentrenado y contiene la entrada `\bibitem{vgg}` para el artículo de Simonyan y Zisserman, pero el texto solo utiliza `\cite{tfdsflowers}`. El README operativo existe únicamente en `vgg16_tf_flowers/README.md`; sus comandos corresponden a scripts reales, aunque presupone que el lector conoce el directorio de trabajo, no menciona `requirements.txt`, fija implícitamente una ubicación de Drive y solo ofrece `pdflatex`.

La validación estricta requiere `report/reporte_vgg16.pdf`, mientras que Tectonic genera por defecto `main.pdf`. Por tanto, la alternativa con Tectonic debe incluir el paso explícito que conserva el nombre esperado por el validador.

## Goals / Non-Goals

**Goals:**

- Relacionar la descripción de VGG16 con su fuente académica mediante una cita en contexto.
- Evitar entradas bibliográficas sin uso y citas indefinidas.
- Hacer que el README pueda seguirse desde una copia limpia sin adivinar el directorio de trabajo.
- Documentar con precisión el flujo Colab, el flujo local, la compilación y el empaquetado.
- Conservar compatibilidad con los scripts y validaciones existentes.

**Non-Goals:**

- Añadir nuevas referencias bibliográficas o cambiar el formato bibliográfico.
- Cambiar el modelo VGG16, sus pesos, arquitecturas, notebooks o resultados.
- Introducir un nuevo gestor de entornos, Makefile o sistema de construcción.
- Crear un README raíz duplicado cuando el entregable autocontenido ya se documenta en `vgg16_tf_flowers/README.md`.
- Cambiar versiones de `requirements.txt`.

## Decisions

### 1. Citar VGG16 en su primera introducción metodológica

Se añadirá `\cite{vgg}` a la primera oración de metodología que afirma que los modelos emplean VGG16 preentrenada. Esa ubicación vincula la arquitectura con la fuente original y evita insertar una cita tardía en la conclusión.

Alternativa considerada: eliminar la entrada bibliográfica. Se descarta porque el artículo es la fuente primaria adecuada para la arquitectura central del trabajo.

### 2. Mantener un único README del entregable

Se actualizará `vgg16_tf_flowers/README.md` en vez de crear un README raíz. El directorio `vgg16_tf_flowers/` es la unidad ejecutable y empaquetable, y el validador exige específicamente su README.

Alternativa considerada: duplicar instrucciones en la raíz. Se descarta para evitar dos fuentes que puedan divergir.

### 3. Separar claramente Colab y ejecución local

El README indicará que:

- Los notebooks esperan `/content/drive/MyDrive/vgg16_tf_flowers`.
- Si la carpeta usa otro nombre o ruta, debe ajustarse la celda `%cd` y, en su caso, `RAIZ_DRIVE`.
- Para utilidades locales, el usuario debe situarse en la raíz de `vgg16_tf_flowers`.
- `python3 -m pip install -r requirements.txt` prepara el entorno local; Colab gestiona su entorno mediante las celdas del notebook.

Esto elimina la ambigüedad actual entre la raíz del repositorio y la raíz del subproyecto.

### 4. Documentar dos compiladores sin ocultar la salida requerida

El flujo principal conservará los dos pases de `pdflatex -jobname=reporte_vgg16 main.tex`. Como alternativa se documentará:

```bash
tectonic main.tex
cp main.pdf reporte_vgg16.pdf
```

El segundo comando es necesario porque `validate_submission.py --strict` busca `report/reporte_vgg16.pdf`. Se explicará que Tectonic resuelve internamente las repeticiones necesarias.

### 5. Verificar instrucciones contra el comportamiento real

La revisión comprobará:

- existencia de todos los scripts y archivos mencionados;
- que `--strict` sea una opción válida;
- que `package_submission.py` cree `VGG16_tf_flowers_entrega.zip` en el directorio padre de `vgg16_tf_flowers/`;
- que las instrucciones de compilación produzcan el PDF exigido;
- que ambas claves bibliográficas aparezcan al menos una vez en `\cite{...}` y que la compilación carezca de referencias indefinidas.

## Risks / Trade-offs

- [El README puede depender de herramientas no instaladas] → Presentar `pdflatex` y Tectonic como alternativas, sin afirmar que se instalan con `requirements.txt`.
- [La ruta de Drive puede cambiar] → Documentar la ruta esperada y los dos valores que deben adaptarse.
- [El PDF de Tectonic puede quedar con nombre incorrecto] → Incluir explícitamente la copia a `reporte_vgg16.pdf`.
- [Duplicar instrucciones puede causar divergencia] → Mantener un único README y contrastarlo con scripts y notebooks durante la validación.
- [La cita podría agregarse en un lugar poco relacionado] → Situarla en la primera introducción metodológica de VGG16.
