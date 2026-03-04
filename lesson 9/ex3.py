import csv
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent

data_file = BASE_DIR / "users.csv"


with open(data_file, mode="r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=";", quotechar='"')
    data = list(reader)


for row in data:
    print(row)
    row["name"] = row["name"].upper()


with open(data_file, mode="w", encoding="utf-8", newline="") as csvfile:
    fieldnames = data[0].keys()

    writer = csv.DictWriter(csvfile, delimiter=";", quotechar='"', fieldnames=fieldnames)
    writer.writeheader()  # Запись заголовка
    writer.writerows(data)  # Запись данных
