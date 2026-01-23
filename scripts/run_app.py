import subprocess
from pathlib import Path

def main():
    app_dir = Path(__file__).parent.parent / "apps" / "stremlit_ui"

    cmd = [
        "streamlit", "run",
        "Home.py"
    ]

    subprocess.run(cmd, cwd=app_dir, check=True)

if __name__ == "__main__":
    main()
