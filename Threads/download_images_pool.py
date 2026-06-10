from concurrent.futures import ThreadPoolExecutor
import threading
import time
from pathlib import Path

import requests

URL = "https://storage.yandexcloud.net/bookshelf/previews/129/preview.png"
COUNT = 10
FOLDER = Path(__file__).parent / "images"
FOLDER.mkdir(parents=True, exist_ok=True)

def download_image(url: str, path: Path) -> None:
    thread_name = threading.current_thread().name
    print(f"{thread_name} started")
    r = requests.get(url)
    with open(path, 'wb') as f:
        f.write(r.content)
    print(f"    {thread_name} ended\n", end="")


def main_no_threads() -> None:
    for i in range(COUNT):
        download_image(URL, FOLDER / f"python-{i}.jpg")
    print()


def main_with_threads() -> None:
    with ThreadPoolExecutor() as executor:
        for i in range(COUNT):
            executor.submit(download_image, URL, FOLDER / f"python-{i}.jpg")



if __name__ == '__main__':
    start = time.perf_counter()
    main_with_threads()
    end = time.perf_counter()
    print(f"Total time: {(end - start) * 1000:.2f} ms")
