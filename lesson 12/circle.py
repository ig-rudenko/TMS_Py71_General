from dataclasses import dataclass
from typing import Any

Number = int | float


@dataclass
class Point:
    x: Number
    y: Number

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other) -> bool:
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        raise TypeError(f"Нельзя сравнивать Point с {type(other)}")

    def from_origin(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __mul__(self, other):
        if isinstance(other, Number):
            return Point(self.x * other, self.y * other)
        raise TypeError(f"Нельзя умножать Point с {type(other)}")


@dataclass
class Vector:
    p1: Point
    p2: Point

    def __str__(self):
        return f"<{self.p2.x - self.p1.x}, {self.p2.y - self.p1.y}>"

    @classmethod
    def from_numbers(cls, x1: Number, y1: Number, x2: Number, y2: Number):
        return cls(Point(x1, y1), Point(x2, y2))

    def __add__(self, other: Any) -> Vector:
        if isinstance(other, Vector):
            return Vector.from_numbers(
                0, 0,
                self.p2.x - other.p1.x + other.p2.x - other.p1.x,
                self.p2.y - other.p1.y + other.p2.y - other.p1.y,
            )
        raise TypeError(f"Нельзя сравнивать Vector с {type(other)}")

    def __radd__(self, other) -> Vector:
        return self.__add__(other)

    def __iadd__(self, other) -> Vector:
        return self.__add__(other)


p1 = Point(x=0, y=0)
p2 = Point(x=2, y=2)
p3 = Point(x=4, y=6)

v1 = Vector(p1, p2)
v2 = Vector(p1, p3)
v3 = Vector.from_numbers(2, 6, 6, 2)

print(v1)
print(v2)
print(v3)


print(v1 + v2)