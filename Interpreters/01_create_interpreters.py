import os

from concurrent import interpreters

global_object = "hello world"
print("PID: ", os.getpid())
print("Interpreter: ", interpreters.get_current().id)


def run_in_interpreter(x, y):
    from interpreter_func import calculate

    queue = globals()["queue"]
    data = queue.get()

    result = calculate(**data)

    queue.put({"DATA": result})


def main():
    queue = interpreters.create_queue()

    worker = interpreters.create()
    worker.prepare_main(queue=queue)

    queue.put({"x": 1, "y": 2})

    try:
        thread = worker.call_in_thread(run_in_interpreter, 1, 2)
        thread.join()

        result = queue.get()
        print(result)

    finally:
        worker.close()


if __name__ == "__main__":
    main()
