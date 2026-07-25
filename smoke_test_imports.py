# smoke_test_imports.py — backend/ folder ke root me rakho, phir run karo

import os
import sys
import importlib
import traceback

# Django setup (agar zaroorat pare)
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

EXCLUDE_DIRS = {"venv", "__pycache__", "migrations", ".vscode", "logs"}

errors = []
success = []

for root, dirs, files in os.walk(BASE_DIR):
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

    for file in files:
        if (
            not file.endswith(".py")
            or file == "manage.py"
            or file == os.path.basename(__file__)
        ):
            continue

        filepath = os.path.join(root, file)
        rel_path = os.path.relpath(filepath, BASE_DIR)

        module_path = rel_path.replace(os.sep, ".").rsplit(".py", 1)[0]

        if module_path.endswith("__init__"):
            module_path = module_path.rsplit(".__init__", 1)[0]

        if not module_path:
            continue

        try:
            importlib.import_module(module_path)
            success.append(module_path)
        except Exception as e:
            errors.append((module_path, str(e), traceback.format_exc()))

print("=" * 70)
print(f"✅ SUCCESSFULLY IMPORTED: {len(success)} modules")
print("=" * 70)
print(f"❌ FAILED: {len(errors)} modules\n")

for mod, err, tb in errors:
    print(f"--- {mod} ---")
    print(f"   ERROR: {err}")
    print()

if errors:
    print("\n" + "=" * 70)
    print("FULL TRACEBACKS (copy these to fix):")
    print("=" * 70)
    for mod, err, tb in errors:
        print(f"\n### {mod} ###")
        print(tb)
