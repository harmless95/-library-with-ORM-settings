from main_file.models import Students, Books, Authors, ReceivingBooks
from main_file.session_file import session


def give_book_student(students, books):
    for book in books:
        receiving_book = ReceivingBooks()
        receiving_book.book = book
        receiving_book.student = students
        session.add(receiving_book)

def give_my_book():
    # Находим учеников по именам
    vitaly = session.query(Students).filter(Students.name=="Виталий").one()
    vladimir = session.query(Students).filter(Students.name=="Владимир").one()
    ilya = session.query(Students).filter(Students.name=="Илья").one()
    pavel = session.query(Students).filter(Students.name=="Павел").one()
    sofia = session.query(Students).filter(Students.name=="София").one()

    # Ищем книги по требованию учеников
    book_to_vitaly = session.query(Books).join(Authors).filter(Authors.surname=="Достоевский").all()
    book_to_vladimir = session.query(Books).join(Authors).filter(Authors.name=="Александр").all()
    book_to_ilya = session.query(Books).filter(Books.name=="Парус").all()
    book_to_pavel = session.query(Books).filter((Books.release_date>=1840) & (Books.release_date<=1850)).all()
    book_to_sofia = session.query(Books).join(Authors).filter(Authors.name=="Лександр", Authors.surname=="Пушкин").all()

    list_students = [vitaly, vladimir, ilya, pavel, sofia]
    list_books = [book_to_vitaly, book_to_vladimir, book_to_ilya, book_to_ilya, book_to_pavel, book_to_sofia]

    # Добавляем книги ученикам
    for i in range(len(list_students)):
        give_book_student(list_students[i], list_books[i])
    session.commit()