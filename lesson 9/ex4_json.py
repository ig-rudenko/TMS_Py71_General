import json
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent

filepath = BASE_DIR / "users.json"

with open(filepath, mode="r", encoding="utf-8") as f:
    data = json.load(f)


print(type(data))

for user in data:
    print(user)
    user["name"] = user["name"].upper() + " 🍅"


with open(filepath, mode="w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
