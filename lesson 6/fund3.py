numbers = [5, 0, 16, 99]

def positive_sum(numbers: list[int | float]) -> int | float:
    summ = 0
    for number in numbers:
        if number <= 0:
            # Пропускает завершение текущей итерации
            continue
        summ += number
    return summ  # Возврат


def sum_a_b(a: int | float, b: int | float) -> int | float:  # 2, 6
    print(numbers)
    return a + b


def mul_a_b(a, b):
    return a + b


result = sum_a_b(2, 6)
print(result)
