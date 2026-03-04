u4 = "user4"

# Индексы         0        1        2     3   4
users_names = ("user1", "user2", "user3", u4, 1)

print(type(users_names))

# users_names[3] -> u4 -> "user4"
print(users_names[3])

# =========================================================

# users_names[3] = "new user1"  Нельзя менять элемены кортежа❗️❗️❗️
print(users_names[3])

list_length = len(users_names)
last_index = list_length - 1

print("Длина списка:", list_length, "Последний индекс:", last_index)

print("Последний элемент:", users_names[last_index])
print("Последний элемент:", users_names[-1])
print("Первый элемент:", users_names[0])
print("Первый элемент:", users_names[-5])

# От 0 (включительно) до 3 (не включительно) индекса.
new_list = users_names[0:3]
print(new_list)

# От 1 (включительно) до конца списка.
print(users_names[1:])

# От начала списка, до 2 (не включительно) индекса.
print(users_names[:2])

# От начала списка, до последнего (не включительно).
print(users_names[:-1])

print(type(users_names))


# Пустой кортеж
empty_tuple = ()

print(type(empty_tuple), empty_tuple)