import subprocess
from pathlib import Path

def main():
    exec_dir = Path(__file__).parent.parent

    cmd = ["pip", "install","-r", "requirements.txt"]

    subprocess.run(cmd, cwd=exec_dir, check=True)

if __name__ == "__main__":
    main()