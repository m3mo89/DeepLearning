## ADDED Requirements

### Requirement: Every bibliography entry is cited in context
El reporte SHALL utilizar cada clave declarada mediante `\bibitem` en al menos una cita del cuerpo, y la cita SHALL aparecer junto a la afirmación que sustenta.

#### Scenario: VGG16 is introduced
- **WHEN** la metodología indica que los modelos usan VGG16 preentrenada
- **THEN** el texto cita `\cite{vgg}` y la referencia de Simonyan y Zisserman deja de estar huérfana

#### Scenario: Report is compiled
- **WHEN** se compila `report/main.tex`
- **THEN** la bibliografía contiene las referencias de `tfdsflowers` y `vgg` sin citas indefinidas

### Requirement: README identifies the correct execution root
El README SHALL indicar que los comandos de generación, validación y empaquetado se ejecutan desde la raíz del directorio `vgg16_tf_flowers/`.

#### Scenario: User follows a local command
- **WHEN** el usuario prepara resultados, valida o empaqueta la entrega
- **THEN** puede identificar el directorio de trabajo correcto antes de ejecutar `scripts/...`

### Requirement: README documents local prerequisites
El README SHALL mencionar Python 3 y SHALL proporcionar el comando basado en `requirements.txt` para preparar un entorno local, distinguiéndolo del entorno administrado por los notebooks en Colab.

#### Scenario: User prepares a local environment
- **WHEN** el usuario decide ejecutar las utilidades o dependencias localmente
- **THEN** encuentra `python3 -m pip install -r requirements.txt` y entiende que necesita además un compilador LaTeX para producir el PDF

### Requirement: README explains the Colab path contract
El README SHALL documentar la ruta de Google Drive esperada por los notebooks y SHALL indicar qué valores adaptar cuando la carpeta se ubique en otro lugar.

#### Scenario: Project uses the expected Drive path
- **WHEN** la carpeta está en `/content/drive/MyDrive/vgg16_tf_flowers`
- **THEN** los notebooks pueden ejecutarse sin modificar sus celdas de ruta

#### Scenario: Project uses a different Drive path
- **WHEN** la carpeta tiene otro nombre o ubicación
- **THEN** el README indica que se deben actualizar `%cd` y `RAIZ_DRIVE` de forma consistente

### Requirement: README provides reproducible report compilation
El README SHALL documentar comandos que produzcan `report/reporte_vgg16.pdf` mediante `pdflatex` o Tectonic.

#### Scenario: User compiles with pdflatex
- **WHEN** `pdflatex` está disponible
- **THEN** dos pases con `-jobname=reporte_vgg16` producen el PDF requerido

#### Scenario: User compiles with Tectonic
- **WHEN** Tectonic está disponible en lugar de `pdflatex`
- **THEN** el README explica cómo compilar `main.tex` y conservar el resultado como `reporte_vgg16.pdf`

### Requirement: README accurately describes validation and packaging
El README SHALL distinguir la validación estructural de la validación estricta y SHALL indicar la ubicación real del ZIP creado por el empaquetador.

#### Scenario: User packages a complete submission
- **WHEN** ejecuta `python3 scripts/package_submission.py` desde `vgg16_tf_flowers/`
- **THEN** entiende que primero se ejecuta la validación estricta y que `VGG16_tf_flowers_entrega.zip` se crea en el directorio padre
