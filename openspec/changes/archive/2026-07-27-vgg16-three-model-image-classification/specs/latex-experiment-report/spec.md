## ADDED Requirements

### Requirement: Complete academic report
The LaTeX document SHALL describe the public dataset, preprocessing, split strategy, shared frozen VGG16 backbone, each classifier head and its justification, training protocol, evaluation definitions, results, analysis, conclusion, and references.

#### Scenario: Review report source
- **WHEN** the final report source is inspected
- **THEN** every required activity topic appears in a dedicated section and claims about performance reference generated evidence

### Requirement: Architecture documentation
The report SHALL include a separate architecture image and layer/parameter description for each model, clearly distinguishing the unchanged convolutional section from the modified classifier head.

#### Scenario: Compare architecture figures
- **WHEN** a reader views the three model diagrams
- **THEN** the same VGG16 backbone is visible in all three and each head's neuron counts, activations, and dropout are identifiable

### Requirement: Formula and multiclass explanation
The report SHALL present formulas for Accuracy, Precision, Recall, and F1 Score and SHALL explain how binary confusion-matrix quantities are extended to five classes and aggregated.

#### Scenario: Interpret reported F1
- **WHEN** a reader checks the evaluation methodology
- **THEN** the report states that per-class metrics use one-versus-rest and that macro F1 is the primary comparison metric

### Requirement: Generated results in tables and figures
The report SHALL include a comparative metric table, per-class results, confusion matrices, learning curves, class-distribution histograms, confidence histograms, and model-comparison charts generated from experiment outputs.

#### Scenario: Refresh experiment results
- **WHEN** metrics and figures are regenerated and the report is rebuilt
- **THEN** tables and conclusions reflect the actual exported results without manually fabricated values

### Requirement: Justified conclusion
The conclusion SHALL identify the best-performing model only after all evaluations complete and SHALL justify it using macro F1, supporting metrics, class behavior, overfitting evidence, and model complexity.

#### Scenario: Finalize conclusion
- **WHEN** all three result files are present
- **THEN** the report names the rule-selected winner and discusses both its advantages and observed limitations

### Requirement: Reproducible submission package
The deliverable SHALL include report source and PDF, exactly six executable Colab notebooks (Train and Test for each of three models), dependency/configuration information, generated figures and metrics, all three trained weight files, checksums, and execution instructions.

#### Scenario: Validate final package
- **WHEN** the submission validation command runs
- **THEN** it fails on any missing Train/Test notebook, artifact, or unresolved placeholder and succeeds only when the package can be traced to three completed model runs
