list1 = [1, 2, 3, 4, 5]


# for el in list1:
# ========================================
_index = 0
_iterator = iter(list1)
while True:
    try:
        el = next(_iterator)
        # ========================================

        print(el)

        # ========================================
    except StopIteration:
        break
    _index += 1
# ========================================
