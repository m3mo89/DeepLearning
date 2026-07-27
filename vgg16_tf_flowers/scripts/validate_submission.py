#!/usr/bin/env python3
"""Valida estructura; --strict exige artefactos producidos por entrenamiento."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--strict", action="store_true")
args = parser.parse_args()
errors = []

for model in "ABC":
    for kind in ("Train", "Test"):
        path = ROOT / "notebooks" / f"VGG16_Modelo_{model}_{kind}.ipynb"
        if not path.exists():
            errors.append(f"Falta {path.relative_to(ROOT)}")
            continue
        try:
            nb = json.loads(path.read_text())
            source = "\n".join("".join(c.get("source", [])) for c in nb["cells"])
            if "VGG16" not in source or model not in source:
                errors.append(f"Contenido inesperado en {path.name}")
        except Exception as exc:
            errors.append(f"Notebook inválido {path.name}: {exc}")

required_source = [
    ROOT / "requirements.txt",
    ROOT / "config" / "experiment.json",
    ROOT / "report" / "main.tex",
    ROOT / "README.md",
]
for path in required_source:
    if not path.exists():
        errors.append(f"Falta {path.relative_to(ROOT)}")

if args.strict:
    for model in "ABC":
        required = [
            ROOT / "weights" / f"modelo_{model}.keras",
            ROOT / "weights" / f"modelo_{model}_best.weights.h5",
            ROOT / "results" / f"modelo_{model}_metricas.json",
            ROOT / "results" / f"modelo_{model}_metadata.json",
            ROOT / "figures" / f"arquitectura_modelo_{model}.png",
            ROOT / "figures" / f"matrices_confusion_modelo_{model}.png",
        ]
        for path in required:
            if not path.exists() or path.stat().st_size == 0:
                errors.append(f"Falta artefacto real {path.relative_to(ROOT)}")
        meta_path = ROOT / "results" / f"modelo_{model}_metadata.json"
        if meta_path.exists():
            meta = json.loads(meta_path.read_text())
            for filename in (f"modelo_{model}.keras", f"modelo_{model}_best.weights.h5"):
                path = ROOT / "weights" / filename
                key = filename + "_sha256"
                if path.exists() and hashlib.sha256(path.read_bytes()).hexdigest() != meta.get(key):
                    errors.append(f"Hash incorrecto: {filename}")
    for path in [ROOT / "report" / "resultados_generados.tex", ROOT / "report" / "reporte_vgg16.pdf"]:
        if not path.exists() or path.stat().st_size == 0:
            errors.append(f"Falta {path.relative_to(ROOT)}")

if errors:
    print("VALIDACIÓN FALLIDA")
    for error in errors:
        print("-", error)
    raise SystemExit(1)
print("VALIDACIÓN CORRECTA" + (" (entrega completa)" if args.strict else " (estructura y fuentes)"))

