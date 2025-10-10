from pathlib import Path
import shutil

def main():
    dir_path = Path(__file__).parent.parent / "src" / "tools" / "config"
    print(dir_path)

    src_file = dir_path / ".env.example"
    dst_file = dir_path / ".env"

    if not dst_file.exists():
        shutil.copy(src_file, dst_file)

if __name__ == "__main__":
    main()
