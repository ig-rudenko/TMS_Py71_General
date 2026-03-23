list1 = [1, 2, 3, 4, 5]

text = "Hello, World!"

iter_list = iter(list1)
iter_text = iter(text)


print(next(iter_list))  # 1
print(next(iter_list))  # 2
print(next(iter_list))  # 3
print(next(iter_list))  # 4
print(next(iter_list))  # 5
print(next(iter_list))  # 6  ❌
print(next(iter_list))  # 7
