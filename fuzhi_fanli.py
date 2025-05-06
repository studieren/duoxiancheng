import shutil
import threading, logging
from pathlib import Path

lock = threading.Lock()

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="errors.log",  # 日志文件的名称
    encoding="utf-8",
)


def copy_file(file: Path, source_dir: Path, target_dir: Path, block_size):
    file_name = file.relative_to(source_dir)
    target_file = target_dir / file_name
    with lock:
        target_file.parent.mkdir(parents=True, exist_ok=True)

    if target_file.exists():
        return
    try:
        with file.open("rb") as f, target_file.open("wb") as fp:
            while True:
                data = f.read(block_size)
                if data:
                    fp.write(data)
                else:
                    break
    except Exception as e:
        logging.error(f"error file{file}")
    else:
        print(f"copy {file} to {target_file}")


def list_files(file_dir: Path):
    return [file for file in file_dir.rglob("*.*") if file.exists()]


if __name__ == "__main__":
    file_dir = Path(r"C:\Users\90539\Pictures\诗诗")
    target_dir = Path(r"E:\诗诗")
    files_list = list_files(file_dir)
    block_size = 1024 * 1024
    for file in files_list:
        copy_pro = threading.Thread(
            target=copy_file,
            args=(file, file_dir, target_dir, block_size),
        )
        copy_pro.start()
