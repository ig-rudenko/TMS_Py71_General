import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

FOLDER = Path(__file__).parent / "files"
FOLDER.mkdir(parents=True, exist_ok=True)


def generate_test_files_data():
    for i in range(1, 11):
        with open(FOLDER / f"file-{i}.txt", "w") as f:
            for j in range(1, 100):
                f.write(f"row {i}\n")


def copy_file_data(file_path: Path, main_fd, lock: threading.Lock):
    print(f"Start to copy file {threading.current_thread().name}")
    time_limit = 50  # ms

    with open(file_path) as f:
        while True:

            with lock:
                print("lock acquired")
                s = time.monotonic()

                print(f"{(time.monotonic() - s) * 1000} ms")
                while (time.monotonic() - s) * 1000 < time_limit:
                    line = f.readline()
                    if not line:
                        break
                    main_fd.write(line)
                    time.sleep(0.01)

            print("lock released")
            time.sleep(0.01)

            if not line:
                break

    print(f"Finished {threading.current_thread().name}")


def main():
    lock = threading.Lock()

    with open(FOLDER / "main.txt", "w") as f:

        with ThreadPoolExecutor() as executor:
            for file_path in FOLDER.glob("file-*.txt"):
                executor.submit(copy_file_data, file_path, f, lock)


if __name__ == '__main__':
    main()
