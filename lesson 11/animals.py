import time
from abc import ABC, abstractmethod


class BaseAnimal:
    def __init__(self, name: str, color: str, age: int) -> None:
        self.name = name
        self.color = color
        self.age = age


class BasicActionMixin(ABC):

    @abstractmethod
    def say(self): ...

    @abstractmethod
    def move(self): ...

    @abstractmethod
    def sleep(self, minutes: int) -> None: ...

    @abstractmethod
    def eat(self, value): ...


class FlyingActionMixin(ABC):
    @abstractmethod
    def fly(self): ...

    def move(self):
        self.fly()


class Dog(BaseAnimal, BasicActionMixin):

    def sleep(self, minutes: int) -> None:
        pass

    def eat(self, value):
        pass

    def say(self):
        print("Гав")

    def move(self):
        print("Собака бежит")


class Cat(BaseAnimal, BasicActionMixin):

    def eat(self, value):
        pass

    def sleep(self, minutes: int) -> None:
        pass

    def say(self):
        print("Мяу")

    def move(self):
        print("Кот бежит")


class Bird(BaseAnimal, FlyingActionMixin, BasicActionMixin):
    def __new__(cls, *args, **kwargs):
        print("new", args, kwargs)
        return super().__new__(cls)

    def sleep(self, minutes: int) -> None:
        print("Птичка спит")
        time.sleep(minutes)
        print("Птичка проснулась")

    def eat(self, value):
        pass

    def say(self):
        print("Чирик")

    def fly(self):
        print("Птица летит")


bird = Bird("Воробей", "серый", 1)

bird.move()

bird.sleep(1)
