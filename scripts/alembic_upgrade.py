import subprocess
import sys
from pathlib import Path

def main():
    migrations_dir = Path(__file__).parent.parent / "apps" / "py_trader" / "data" / "migrations"

    cmd = [
        "alembic", "upgrade",
        "head"
    ]

    subprocess.run(cmd, cwd=migrations_dir, check=True)

if __name__ == "__main__":
    main()