## ADDED Requirements

### Requirement: Reproducible public dataset
The experiment SHALL load `tf_flowers` from TensorFlow Datasets and SHALL create persistent stratified train, validation, and test partitions using a documented seed.

#### Scenario: First dataset preparation
- **WHEN** the preparation workflow runs without an existing split manifest
- **THEN** it creates 70/15/15 stratified partitions and saves the example assignments, labels, class names, dataset version, and seed

#### Scenario: Repeated dataset preparation
- **WHEN** the preparation workflow runs with an existing valid split manifest
- **THEN** it reconstructs the same partitions without assigning any example to more than one split

### Requirement: Common VGG16 input pipeline
The system SHALL transform every example into a 224×224 RGB tensor and SHALL apply VGG16 preprocessing, with augmentation limited to the training split.

#### Scenario: Evaluation input
- **WHEN** an example belongs to validation or test
- **THEN** the pipeline resizes and preprocesses it without random augmentation

#### Scenario: Training input
- **WHEN** an example belongs to training
- **THEN** the pipeline applies the configured common augmentation before VGG16 preprocessing

### Requirement: Frozen convolutional backbone
All three models SHALL use the same ImageNet-pretrained VGG16 convolutional backbone with `include_top=False`, and every backbone layer SHALL remain non-trainable throughout training.

#### Scenario: Model construction
- **WHEN** any of the three model variants is built
- **THEN** its VGG16 layers are frozen and only its classifier head contains trainable parameters

### Requirement: Three distinct multiclass heads
The system SHALL provide exactly three named classifier variants after a common `GlobalAveragePooling2D` layer: A with only a five-unit softmax output, B with a 256-unit ReLU layer and five-unit softmax output, and C with 512-unit ReLU, 0.5 dropout, 128-unit ReLU, and five-unit softmax output.

#### Scenario: Architecture inspection
- **WHEN** model summaries are generated
- **THEN** the convolutional section is identical across variants and the three heads match their specified neurons and activations

### Requirement: Comparable training protocol
The system SHALL train each variant using identical data partitions, preprocessing, optimizer settings, loss, epoch budget, and checkpoint-selection policy.

#### Scenario: Three-model training run
- **WHEN** the experiment trains variants A, B, and C
- **THEN** each run uses Adam, sparse categorical crossentropy, the shared configuration, and validation-only callbacks for checkpoint selection

### Requirement: Persistent experiment artifacts
Each completed model run SHALL save its best weights, loadable model, training history, configuration, parameter counts, best epoch, runtime, and integrity hash.

#### Scenario: Successful model completion
- **WHEN** a model finishes training and its best checkpoint is restored
- **THEN** all required artifacts are written under that model's stable output directory and are referenced by the delivery manifest

### Requirement: Six template-derived Colab notebooks
The deliverable SHALL contain exactly one standalone Train notebook and one standalone Test notebook for each model A, B, and C, derived through minimal necessary edits from the instructor-provided `VGG16_Train.ipynb` and `VGG16_Test.ipynb`.

#### Scenario: Inspect notebook lineage
- **WHEN** the six notebooks are compared with the instructor templates
- **THEN** their instructional flow remains recognizable and changes are limited to dataset handling, multiclass outputs, the specified dense head, training artifacts, evaluation metrics, and required visualizations

#### Scenario: Execute a model pair
- **WHEN** a user runs one model's Train notebook followed by its Test notebook in Colab
- **THEN** the Train notebook produces that model's weights and the Test notebook loads those weights and evaluates the corresponding model without depending on another model's notebook
