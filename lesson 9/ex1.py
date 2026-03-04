import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent

filepath = BASE_DIR / "test.txt"

with open(filepath, mode="rt", encoding="utf-8") as f:
    data = f.read()

print(len(data))
print(type(data))
print(data)

# hex_data = data.hex()
# print(hex_data)
# print(type(hex_data))
# print(len(hex_data))


some_data = b"\x55\x42\x0a"

print(some_data)
hex_data2 = some_data.hex()

print(hex_data2)

print(bytes.fromhex(hex_data2))

