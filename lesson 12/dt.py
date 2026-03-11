from datetime import datetime, date, time, timedelta
import json
from dataclasses import dataclass, field


@dataclass(kw_only=True)
class Book:
    index: str
    title: str
    authors: str
    year: int
    tags: list[str] = field(default_factory=list)
    desc: str = ""
    created_at: datetime = field(default_factory=datetime.now)

    def json(self):
        return {
            **self.__dict__,
            "created_at": self.created_at.isoformat()
        }


book_2 = Book(index="978-5-4461-1639-3", authors="Билл Любанович", title="Простой python", year=2020, tags=["python", "api"])

json_data = json.dumps(book_2.json(), ensure_ascii=False)
print("JSON", json_data)

now = datetime.now()
print("ISO 8601:", now.isoformat())
print("Timestamp:", now.timestamp())

print(now.strftime("%d %B %A"))

dt2 = datetime.strptime("09/04/2025 20:02:49", "%d/%m/%Y %H:%M:%S")
print(dt2)
