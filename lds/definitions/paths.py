import os.path
from pathlib import Path

# Get directory of paths.py ([project_path]/lds/definitions/)
path = os.path.dirname(os.path.abspath(__file__))
# Go up 3 levels ([project_path]/)
for _ in range(2):
    path = Path(path).parent.absolute()
# Get path directory of the python source

ROOT_DIR = path
