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

    def json(self):
        return self.__dict__


@dataclass(kw_only=True)
class Bookshelf:
    books: list[Book] = field(default_factory=list)

    def json(self):
        return {
            "books": [book.json() for book in self.books],
        }


def create_book(*, index: str, title: str, authors: str, year: int, tags: list[str], desc: str = "") -> dict:
    return {
        "index": index,
        "title": title,
        "authors": authors,
        "year": year,
        "tags": tags,
        "desc": desc,
    }


def main():
    book = create_book(index="978-5-4461-1639-3", title="Простой python", authors="Билл Любанович", year=2020,
                       tags=["python", "api"])
    book["pages"] = 592
    print(book["pages"])

    book_2 = Book(index="978-5-4461-1639-3", authors="Билл Любанович", title="Простой python", year=2020,
                  tags=["python", "api"])
    print(book_2)

    bs = Bookshelf(books=[book_2])

    print(bs.books[0].index)

    print(json.dumps(book_2.json(), ensure_ascii=False))


main()
