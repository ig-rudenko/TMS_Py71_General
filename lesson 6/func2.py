
def compare_number(numbers: list[int | float]) -> list[bool | None]:
    results: list[bool | None] = []  # [True, False, None]
    for n in numbers:
        if n > 0:
            results.append(True)
        elif n < 0:
            results.append(False)
        else:
            results.append(None)

    return results


number = 123  # int(input("Enter a number 1: "))
number2 = -23  # int(input("Enter a number 2: "))
number3 = 0  # int(input("Enter a number 3: "))

input_list = [number, number2, number3]


results = compare_number(input_list)

print("Сумма чисел: ", sum(input_list))

number = 123  # int(input("Enter a number 1: "))
number2 = -23  # int(input("Enter a number 2: "))
number3 = 0  # int(input("Enter a number 3: "))

input_list = [number, number2, number3]


results += compare_number(input_list)

mult = 1
for n in input_list:
    mult = mult * n

print("Произведение чисел: ", mult)


print(results)
