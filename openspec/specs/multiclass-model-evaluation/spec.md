# multiclass-model-evaluation Specification

## Purpose
TBD - created by archiving change vgg16-three-model-image-classification. Update Purpose after archive.

## Requirements

### Requirement: Held-out test evaluation
The evaluator SHALL generate final metrics from the untouched test partition and SHALL preserve predicted probabilities, predicted labels, and true labels for every test example.

#### Scenario: Evaluate a trained model
- **WHEN** a best model checkpoint is evaluated
- **THEN** the evaluator emits one prediction record per test example without using test outcomes to retrain or select that checkpoint

### Requirement: Required classification metrics
For every model, the evaluator SHALL calculate Accuracy, class-wise Precision, Recall, and F1 Score, plus macro and weighted averages, using a documented zero-division policy.

#### Scenario: A class receives no predicted samples
- **WHEN** Precision or F1 would otherwise be undefined for a class
- **THEN** the evaluator assigns zero according to `zero_division=0` and keeps the class in all reports

### Requirement: Multiclass confusion matrix
For every model, the evaluator SHALL produce a labeled 5×5 confusion matrix whose rows are actual classes and columns are predicted classes.

#### Scenario: Confusion matrix export
- **WHEN** evaluation completes
- **THEN** the numeric matrix and a readable heatmap are saved with the same fixed class order

### Requirement: Metric consistency
The evaluator SHALL verify computed metrics against the confusion matrix and SHALL explain TP, FP, FN, and TN per class using one-versus-rest interpretation.

#### Scenario: Metrics validation
- **WHEN** metrics are exported
- **THEN** Accuracy equals the confusion-matrix diagonal sum divided by the total and per-class values agree with their one-versus-rest counts within numeric tolerance

### Requirement: Comparative visualizations
The system SHALL export dataset distributions, learning curves, confusion matrices, model metric comparisons, per-class F1 values, and prediction-confidence histograms in report-ready formats.

#### Scenario: Complete experiment visualization
- **WHEN** all three model evaluations and histories exist
- **THEN** the visualization workflow creates consistently styled PNG or PDF figures without manually entered metric values

### Requirement: Evidence-based winner selection
The comparison SHALL select the best model by highest test macro F1, using Accuracy, generalization gap, and trainable parameter count as ordered tie-breakers.

#### Scenario: Rank completed models
- **WHEN** valid results exist for all three variants
- **THEN** the comparison records the ranking, decisive metric values, tie-breakers if used, and the rationale for the winning model
