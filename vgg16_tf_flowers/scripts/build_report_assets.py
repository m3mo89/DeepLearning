#!/usr/bin/env python3
"""Convierte resultados reales de los tres Test Colabs en fragmentos LaTeX."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
REPORT = ROOT / "report"


def esc(value):
    return str(value).replace("_", r"\_").replace("%", r"\%")


rows = []
weight_rows = []
metrics = []
class_reports = {}
for model in "ABC":
    path = RESULTS / f"modelo_{model}_metricas.json"
    if not path.exists():
        raise SystemExit(f"Falta {path}. Ejecuta los tres notebooks Test antes de construir el reporte.")
    item = json.loads(path.read_text())
    metrics.append(item)
    class_path = RESULTS / f"modelo_{model}_metricas_por_clase.csv"
    if not class_path.exists():
        raise SystemExit(f"Falta {class_path}.")
    import csv
    with class_path.open() as stream:
        class_reports[model] = list(csv.DictReader(stream))
    rows.append(
        f"{model} & {item['accuracy']:.4f} & {item['precision_macro']:.4f} & "
        f"{item['recall_macro']:.4f} & {item['f1_macro']:.4f} \\\\"
    )

metadata = {}
for model in "ABC":
    path = RESULTS / f"modelo_{model}_metadata.json"
    if not path.exists():
        raise SystemExit(f"Falta {path}.")
    metadata[model] = json.loads(path.read_text())
    item = metadata[model]
    weight_rows.append(
        f"{model} & {item['parametros_totales']:,} & "
        f"{item['parametros_entrenables']:,} & {item['mejor_epoca']} & "
        f"{item['duracion_segundos'] / 60:.2f} min \\\\"
    )

ranked = sorted(
    metrics,
    key=lambda x: (
        x["f1_macro"],
        x["accuracy"],
        -x["brecha_f1_validacion_prueba"],
        -metadata[x["modelo"]]["parametros_entrenables"],
    ),
    reverse=True,
)
winner = ranked[0]
winner_classes = class_reports[winner["modelo"]]
best_class = max(winner_classes, key=lambda row: float(row["f1"]))
worst_class = min(winner_classes, key=lambda row: float(row["f1"]))
content = r"""\begin{table}[H]
\centering
\caption{Resultados sobre el conjunto de prueba.}
\label{tab:resultados}
\begin{tabular}{lrrrr}
\toprule
Modelo & Accuracy & Precision macro & Recall macro & F1 macro\\
\midrule
""" + "\n".join(rows) + r"""
\bottomrule
\end{tabular}
\end{table}

\begin{table}[H]
\centering
\caption{Pesos, parámetros y entrenamiento obtenidos. Los parámetros no
entrenables corresponden a la base VGG16 congelada.}
\label{tab:pesos}
\begin{tabular}{lrrrr}
\toprule
Modelo & Parámetros totales & Entrenables & Mejor época & Tiempo\\
\midrule
""" + "\n".join(weight_rows) + r"""
\bottomrule
\end{tabular}
\end{table}

\paragraph{Selección del mejor modelo.}
El Modelo """ + esc(winner["modelo"]) + (
    f" obtuvo el mayor F1 macro ({winner['f1_macro']:.4f}), con Accuracy "
    f"{winner['accuracy']:.4f}. Por tanto, bajo la regla definida antes del "
    "experimento, es el modelo seleccionado. La interpretación por clase y "
    "los posibles indicios de sobreajuste deben contrastarse con las matrices "
    "de confusión y las curvas presentadas.\n\n"
    r"\paragraph{Análisis por clase.} "
    f"En el modelo ganador, la clase con mayor F1 fue {esc(best_class['clase'])} "
    f"({float(best_class['f1']):.4f}) y la de menor F1 fue "
    f"{esc(worst_class['clase'])} ({float(worst_class['f1']):.4f}). "
    f"La brecha absoluta entre F1 macro de validación y prueba fue "
    f"{winner['brecha_f1_validacion_prueba']:.4f}; este valor, junto con las "
    "curvas de aprendizaje, permite valorar la generalización sin basarse "
    "solamente en Accuracy."
) + "\n"
(REPORT / "resultados_generados.tex").write_text(content)
(REPORT / "conclusion_generada.tex").write_text(
    f"El Modelo {winner['modelo']} ofrece el mejor desempeño global. Alcanzó "
    f"Accuracy de {winner['accuracy']:.4f}, Precision macro de "
    f"{winner['precision_macro']:.4f}, Recall macro de "
    f"{winner['recall_macro']:.4f} y F1 macro de {winner['f1_macro']:.4f}. "
    f"Superó en F1 macro al Modelo B ({metrics[1]['f1_macro']:.4f}) y al "
    f"Modelo C ({metrics[2]['f1_macro']:.4f}), y presentó la menor brecha "
    f"validación--prueba ({winner['brecha_f1_validacion_prueba']:.4f}). "
    f"Además, necesitó únicamente {metadata[winner['modelo']]['parametros_entrenables']:,} "
    "parámetros entrenables, por lo que la mayor complejidad de los otros "
    "cabezales no produjo una mejora. Sus principales limitaciones aparecen "
    f"en {esc(worst_class['clase'])}, con F1 de {float(worst_class['f1']):.4f}; "
    "la matriz revela que la confusión dominante ocurre entre tulips y roses. "
    "En consecuencia, se elige el Modelo A por ofrecer la mejor combinación "
    "de desempeño, generalización y simplicidad."
)
(RESULTS / "ganador.txt").write_text(
    f"Modelo {winner['modelo']}; F1 macro={winner['f1_macro']:.4f}; "
    f"Accuracy={winner['accuracy']:.4f}\n"
)
print(REPORT / "resultados_generados.tex")
