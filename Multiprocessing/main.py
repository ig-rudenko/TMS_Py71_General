import random
import os

import multiprocessing as mp

import time


def generator(work_queue: mp.Queue) -> None:
    try:
        print(f"Starting generator | PID: {os.getpid()}")
        while True:
            work_queue.put(random.randint(0, 100))
            time.sleep(random.random() * 2)  # От 0 до 2 сек. пауза.
    except KeyboardInterrupt:
        pass


def worker_spawner(work_queue: mp.Queue, semaphore: mp.Semaphore) -> None:
    try:
        print(f"Starting worker_spawner | PID: {os.getpid()}")
        worker_number = 1
        while True:
            print(semaphore)
            semaphore.acquire()
            worker_process = mp.Process(target=worker, args=(f"{worker_number}", work_queue, semaphore))
            worker_process.start()
            worker_number += 1

    except KeyboardInterrupt:
        pass


def worker(worker_name: str, work_queue: mp.Queue, semaphore: mp.Semaphore) -> None:
    print(f"Starting worker ({worker_name}) | PID: {os.getpid()}")
    try:
        while True:
            data = work_queue.get()
            print(f"worker ({worker_name}) got data: `{data}`")
            fake_work(data)

    except KeyboardInterrupt:
        pass

    finally:
        semaphore.release()


def fake_work(data):
    time.sleep(random.random() * 0.5 + 0.5)  # Ждём от 0.5 до 1 сек.
    if random.random() < 0.1:  # 10% шанс на ошибку.
        raise ValueError("ERROR!")


def main(worker_limit: int):
    print(f"Starting | PID: {os.getpid()}")

    manager = mp.Manager()

    work_queue = manager.Queue()
    semaphore = mp.Semaphore(worker_limit)

    generator_process = mp.Process(target=generator, args=(work_queue,))
    generator_process.start()

    worker_spawner_process = mp.Process(target=worker_spawner, args=(work_queue, semaphore))
    worker_spawner_process.start()

    try:
        generator_process.join()
        worker_spawner_process.join()
    except KeyboardInterrupt:
        generator_process.terminate()
        generator_process.join()
        worker_spawner_process.terminate()
        worker_spawner_process.join()

    print("Exiting Main Thread")


if __name__ == "__main__":
    main(worker_limit=3)
