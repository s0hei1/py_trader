import subprocess
from pathlib import Path

def main():
    migrations_dir = Path(__file__).parent.parent / "src" / "ui"

    cmd = [
        "streamlit", "run",
        "Home.py"
    ]

    subprocess.run(cmd, cwd=migrations_dir, check=True)

if __name__ == "__main__":
    main()
