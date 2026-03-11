import random
import string


class Human:
    def __init__(self, name: str, age: int):
        self.age = age
        self.name = name

    @staticmethod
    def is_adult(age: int) -> bool:
        return age >= 18

    @staticmethod
    def get_random_name() -> str:
        return "".join(random.choices(string.ascii_letters + string.digits, k=10)).title()

    def work(self):
        print("Живет")

    @classmethod
    def create_from_str(cls, str_data: str):
        name, age = str_data.split(",")
        return cls(name=name, age=int(age))


class Doctor(Human):

    def work(self):
        print("Лечит")


human_1 = Human("Mark", 18)
doctor_1 = Doctor("Igor", 20)


csv_person_info = "Max,21"


name, age = csv_person_info.split(",")
doctor_2 = Doctor(name, int(age))
print(type(doctor_2), doctor_2.name, doctor_2.age)

doctor_3 = Doctor.create_from_str(csv_person_info)
print(type(doctor_3), doctor_3.name, doctor_3.age)


