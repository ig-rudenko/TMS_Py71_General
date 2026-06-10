import os
from concurrent import interpreters

from concurrent.futures import InterpreterPoolExecutor
from itertools import repeat

global_object = "hello world"
print("PID: ", os.getpid())
print("Interpreter: ", interpreters.get_current().id)


def run_in_interpreter(kwargs):
    from interpreter_func import add

    queue = kwargs["queue"]
    data = queue.get()

    return add(**data)


COUNT = 10


def main():
    queue = interpreters.create_queue()

    for i in range(COUNT):
        queue.put({"x": 1 * i, "y": 2 * i})

    with InterpreterPoolExecutor() as executor:
        results = list(executor.map(run_in_interpreter, repeat({"queue": queue}, COUNT)))

    print(results)


if __name__ == "__main__":
    main()
