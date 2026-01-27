import subprocess
import sys
from pathlib import Path


def main():
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
    else:
        message = input("Enter migration message: ").strip()
        if not message:
            print("❌ Migration message cannot be empty.")
            sys.exit(1)

    migrations_dir = Path(__file__).parent.parent / "apps" / "py_trader" / "data" / "migrations"

    add_migrations = [

        "alembic", "revision",
        "--autogenerate",
        "-m", message
    ]

    subprocess.run(add_migrations, cwd=migrations_dir, check=True)

if __name__ == "__main__":
    main()
