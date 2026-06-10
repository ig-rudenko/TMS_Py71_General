import threading
from pathlib import Path

import requests

URL = "https://storage.yandexcloud.net/bookshelf/previews/129/preview.png"
COUNT = 100
FOLDER = Path(__file__).parent / "images"
FOLDER.mkdir(parents=True, exist_ok=True)


def download_image(url: str, path: Path, s: threading.Semaphore) -> None:
    try:
        s.acquire()

        thread_name = threading.current_thread().name
        print(f"{thread_name} started")
        r = requests.get(url)
        with open(path, "wb") as f:
            f.write(r.content)
        print(f"    {thread_name} ended\n", end="")

    finally:
        s.release()


def main(worker_limit: int) -> None:
    semaphore = threading.Semaphore(worker_limit)

    threads = []
    for i in range(COUNT):
        threads.append(
            threading.Thread(
                target=download_image,
                name=f"thread-{i}",
                args=(URL, FOLDER / f"python-{i}.jpg", semaphore),
            )
        )

    for t in threads:
        t.start()

    for t in threads:
        t.join()


if __name__ == "__main__":
    main(worker_limit=1)
