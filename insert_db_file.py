from main_file.models import Authors, Books, Students
from datetime import date

from main_file.session_file import session


def insert_data():
    list_authors = [
        Authors(name="Александр", surname="Пушкин"),
        Authors(name="Фёдор", surname="Достоевский"),
        Authors(name="Николай", surname="Гоголь"),
        Authors(name="Лев", surname="Толстой"),
        Authors(name="Михаил", surname="Лермонтов")
    ]
    list_authors[0].books.extend(
        [
            Books(name="Капитанская дочка",
                  count=5,
                  release_date=date(1836, 1, 1)
                  ),
            Books(name="Дубровский",
                  count=4,
                  release_date=date(1841, 1, 1)),
            Books(name="Пиковая дама",
                  count=8,
                  release_date=date(1834, 1, 1)),
            Books(name="Я вас любил",
                  count=2,
                  release_date=date(1830, 1, 1))
        ]
    ),
    list_authors[1].books.extend(
        [
            Books(name="Братья карамазовы",
                  count=3,
                  release_date=date(1880, 1, 1)),
            Books(name="Преступление и наказание",
                  count=12,
                  release_date=date(1866, 1, 1)),
            Books(name="Белые ночи",
                  count=6,
                  release_date=date(1848, 1, 1)),
            Books(name="Игрок",
                  count=4,
                  release_date=date(1866, 1, 1))
        ]
    ),
    list_authors[2].books.extend(
        [
            Books(name="Мёртвые дущи",
                  count=14,
                  release_date=date(1842, 1, 1)),
            Books(name="Тарас Бульба",
                  count=11,
                  release_date=date(1835, 1, 1)),
            Books(name="Шинель",
                  count=2,
                  release_date=date(1842, 1, 1)),
            Books(name="Нос",
                  count=4,
                  release_date=date(1836, 1, 1))
        ]
    ),
    list_authors[3].books.extend(
        [
            Books(name="Война и мир",
                  count=15,
                  release_date=date(1867, 1, 1)),
            Books(name="Анна Каренина",
                  count=11,
                  release_date=date(1878, 1, 1)),
            Books(name="Детство",
                  count=3,
                  release_date=date(1852, 1, 1)),
            Books(name="После бала",
                  count=6,
                  release_date=date(1911, 1, 1))
        ]
    ),
    list_authors[4].books.extend(
        [
            Books(name="Герои нашего времени",
                  count=9,
                  release_date=date(1840, 1, 1)),
            Books(name="Мцыри",
                  count=5,
                  release_date=date(1840, 1, 1)),
            Books(name="Бородино",
                  count=14,
                  release_date=date(1837, 1, 1)),
            Books(name="Парус",
                  count=12,
                  release_date=date(1841, 1, 1))
        ]
    )
    list_students = [
        Students(name="Виталий",
                 surname="Захаров",
                 email="vitzah@yandex.ru",
                 phone="+79876543211",
                 scholarship=True,
                 average_score=9.0),
        Students(name="Владимир",
                 surname="Петренко",
                 email="vape@yandex.ru",
                 phone="+79876543212",
                 scholarship=True,
                 average_score=3.0),
        Students(name="Илья",
                 surname="Артонов",
                 email="ilar@yandex.ru",
                 phone="+79876543212",
                 scholarship=True,
                 average_score=6.0),
        Students(name="Павел",
                 surname="Иванов",
                 email="pavi@yandex.ru",
                 phone="+79876543211",
                 scholarship=True,
                 average_score=8.5),
        Students(name="София",
                 surname="Деревянко",
                 email="sode@yandex.ru",
                 phone="+79876543214",
                 scholarship=True,
                 average_score=7.5)
    ]
    session.add_all(list_authors)
    session.add_all(list_students)
    session.commit()