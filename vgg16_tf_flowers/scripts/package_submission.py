#!/usr/bin/env python3
"""Valida y empaqueta la entrega completa sin temporales ni secretos."""
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
subprocess.run([sys.executable, ROOT / "scripts" / "validate_submission.py", "--strict"], check=True)
target = ROOT.parent / "VGG16_tf_flowers_entrega.zip"
excluded = {".DS_Store", "__pycache__", ".ipynb_checkpoints"}
with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(ROOT.rglob("*")):
        if path.is_file() and not any(part in excluded for part in path.parts):
            if path.suffix not in {".pyc", ".aux", ".log", ".out", ".toc"}:
                archive.write(path, Path(ROOT.name) / path.relative_to(ROOT))
with zipfile.ZipFile(target) as archive:
    bad = archive.testzip()
    if bad:
        raise SystemExit(f"Archivo ZIP corrupto: {bad}")
print(target)

