from typing import Any, Generator


def number_generator(start: int = 0, stop: int = None, step: int = 1) -> Generator[int, Any, None]:
    print("Start generator")
    value = start
    while True:
        print(f"yield value {value}")
        yield value
        print(f"after yield value {value}")
        value += step
        if stop is not None and value >= stop:
            print("break")
            break


print("create generator")
generator = number_generator(1, 10)
print("after create generator")

print("Start create new gen")
map_value = map(lambda x: x ** 2, (v for v in generator if v % 2 == 0))
print("Stop create new gen")

print(map_value)


for value in map_value:
    print(value)
    if value > 20:
        break
