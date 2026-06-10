import os

from concurrent import interpreters


def calculate(x: int, y: int):
    print("PID: ", os.getpid())
    print("Interpreter: ", interpreters.get_current().id)

    result = 0
    for number in range(20_000_000):
        result += x * y

    return result
