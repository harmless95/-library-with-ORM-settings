from datetime import datetime

from flasgger import APISpec, Swagger
from flask import Flask, jsonify, request
from flask_restful import Api
from werkzeug.serving import WSGIRequestHandler

from main_file.base_file import Base
from main_file.session_file import engine, session
from main_file.models import Students, Authors, Books
from insert_db_file import insert_data
from give_db_file import give_my_book
from logs.logging_app import setup_logger


logger = setup_logger()

app = Flask(__name__)
api = Api(app)

spec = APISpec(
    title="School library",
    version="6.8.1",
    openapi_version="2.0"
)
template = spec.to_flasgger(app)
swagger = Swagger(app, template_file="docs_restapi/swagger_library.json")

# @app.before_request
# def base_metadata():
#     Base.metadata.create_all(engine)

# Взаимодействие с Students
@app.route("/students", methods=["GET"])
def get_all_students():
    try:
        logger.info("Start get all students")
        students = session.query(Students).all()
        list_students = []
        for student in students:
            list_students.append(student.to_json())
        logger.info("Success: retrieved %s students", len(list_students))
        return jsonify(all_students=list_students), 200
    except Exception as ex:
        logger.error("Error occurred while getting all students: %s", str(ex))
        return jsonify({"error": f"message: {str(ex)}"}), 500


@app.route("/student/<int:id>", methods=["GET"])
def get_student_by_id(id: int):
    try:
        logger.info("Start get student by id")
        student = session.query(Students).filter(Students.id == id).one()
        logger.info("Successfully retrieved student with id: %s", id)
        return jsonify(student=student.to_json()), 200
    except Exception as ex:
        logger.error("Error occurred while getting student by id: %s", str(ex))
        return jsonify({"error": f"message: {str(ex)}"}), 500


@app.route("/student/name/<string:name>", methods=["GET"])
def get_student_by_name(name: str):
    try:
        logger.info("Start get student by name")
        students = session.query(Students).filter(Students.name.like(f"%{name}%")).all()
        list_name = [student.to_json() for student in students]
        logger.info("Successfully received students by name: %s, quantity: %d", name, len(list_name))
        return jsonify(name=list_name), 200
    except Exception as ex:
        logger.error("Error occurred while getting student by name: %s", str(ex))
        return jsonify({"error": f"message: {str(ex)}"}), 500


@app.route("/student/<int:id>", methods=["DELETE"])
def delete_student_by_id(id: int):
    try:
        logger.info("Start delete student by id")
        student = session.query(Students).filter(Students.id == id).one_or_none()
        if not student:
            logger.info("Student not found by id: %s", id)
            return jsonify({"message": "Такого ученика нет"}), 400
        session.delete(student)
        session.commit()
        logger.info("Student successfully deleted by id: %s", id)
        return jsonify({"message": "Ученик успешно удален"}), 200
    except Exception as ex:
        session.rollback()
        logger.error("Error deleting student: %s", str(ex))
        return jsonify({"error": f"message: {str(ex)}"}), 500


# Взаимодействие с Books
@app.route("/books", methods=["GET"])
def get_all_books():
    try:
        logger.info("Start get all book")
        books = session.query(Books).all()
        list_books = []
        for book in books:
            list_books.append(book.to_json())
        logger.info("The books have been successfully received, in quantity: %s", len(list_books))
        return jsonify(all_books=list_books), 200
    except Exception as ex:
        logger.error("Error while displaying all books: %s", str(ex))
        return jsonify({"error": f"message: {str(ex)}"}), 500


@app.route("/book/<int:id>", methods=["GET"])
def get_book_by_id(id: int):
    try:
        logger.info("Start get book by id")
        book = session.query(Books).filter(Books.id == id).one()
        logger.info("Book successfully found by id: %s", id)
        return jsonify(book=book.to_json()), 200
    except Exception as ex:
        logger.error("Error when outputting a book by id: %s", str(ex))
        return jsonify({"error": f"message: {str(ex)}"}), 500


@app.route("/book/name/<string:name>", methods=["GET"])
def get_book_by_name(name: str):
    try:
        logger.info("Start get book by name")
        books = session.query(Books).filter(Books.name.like(f"%{name}%")).all()
        list_book = []
        for book in books:
            book_json = book.to_json()
            # Предполагается, что у книги есть связанный автор
            if hasattr(book, 'author') and book.author:
                book_json['author_name'] = book.author.name
                book_json["author_surname"] = book.author.surname
            else:
                book_json['author_name'] = None
                book_json["author_surname"] = None
            list_book.append(book_json)
        logger.info("Book successfully found by name: %s", name)
        return jsonify(name=list_book), 200
    except Exception as ex:
        logger.error("Error searching for book by title: %s", str(ex))
        return jsonify({"error": f"message: {str(ex)}"}), 500


@app.route("/book/<int:id>", methods=["DELETE"])
def delete_book_by_id(id: int):
    try:
        logger.info("Start delete book by id")
        book = session.query(Books).filter(Books.id == id).one_or_none()
        if not book:
            logger.info("Book not found by id: %s", id)
            return ({"message": "Такой книги нет"}), 404
        session.delete(book)
        session.commit()
        logger.info("Book successfully deleted by id: %s", id)
        return jsonify({"message": "Книга успешна удалена"}), 200
    except Exception as ex:
        session.rollback()
        logger.error("Error deleting book by id: %s", str(ex))
        return jsonify({"error": f"message: {str(ex)}"}), 500


@app.route("/book", methods=["POST"])
def add_book():
    logger.info("Start add book")
    if request.method == "POST":
        try:
            all_data = request.json
            logger.info("Received data for adding book: %s", all_data)
            author = all_data["author"].split()
            author_name = author[0]
            author_surname = author[1]
            release_book = datetime.strptime(all_data["release_date"], "%Y, %m, %d").date()
            # Проверяем есть ли такой автор в базе данных
            author_new = session.query(Authors).filter(
                Authors.name == author_name,
                Authors.surname == author_surname
            ).one_or_none()
            # Добавляем автора если нет
            if author_new is None:
                author_new = Authors(name=author_name, surname=author_surname)
                session.add(author_new)
                session.flush()
                logger.info("Added new author: %s %s", author_name, author_surname)
            # Проверяем есть ли такая книга в наличие
            book_new = session.query(Books).filter(
                Books.name==all_data["name"],
            Books.release_date==release_book,
            Books.id_author==author_new.id
            ).one_or_none()
            # Добавляем если не найдено
            if book_new is None:
                book = Books(name=all_data["name"], count=all_data["count"], release_date=release_book, id_author=author_new.id)
                session.add(book)
                logger.info("Added new book: %s", all_data["name"])
            else:
                # Если такая есть увеличиваем кол-во
                book_new.count += all_data["count"]
                logger.info("Updated book count for: %s, new count: %d", all_data["name"], book_new.count)
            session.commit()
            return jsonify({"message": "Книга успешно добавлена"}), 201
        except Exception as ex:
            session.rollback()
            logger.error("Error occurred while adding book: %s", str(ex))
            return jsonify({"error": f"message: {str(ex)}"}), 500
    else:
        return jsonify({"message": "Метод не разрешен"}), 405

@app.route("/book/<int:id>", methods=["PATCH"])
def update_book(id: int):
    logger.info("Start update book")
    if request.method == "PATCH":
        try:
            all_date = request.json
            logger.info("Received data for adding book: %s", all_date)
            # Ищем книгу по id
            book = session.query(Books).filter(Books.id==id).one_or_none()
            if book is None:
                logger.info("Book not found by id: %s", id)
                return jsonify({"message": "Книга не найдена"})
            # Если найдена меняем значения те поля, что есть в базе данных
            for field, value in all_date.items():
                if field == "release_date":
                    value = datetime.strptime(value, "%Y, %m, %d").date()
                if hasattr(book, field):
                    setattr(book, field, value)
            session.commit()
            logger.info("Book %s data updated", id)
            return jsonify({"message": "Данные обновлены"}), 200
        except Exception as ex:
            session.rollback()
            logger.error("An error occurred while updating the book by id: %s", id)
            return jsonify({"error": f"message : {str(ex)}"}), 500
    else:
        return jsonify({"message": "Ошибка метода"}), 405


# Взаимодействие с Authors
@app.route("/authors", methods=["GET"])
def get_all_authors():
    try:
        logger.info("Start get all authors")
        authors = session.query(Authors).all()
        list_authors = []
        for author in authors:
            list_authors.append(author.to_json())
        logger.info("All authors have been displayed successfully, quantity: %s", len(list_authors))
        return jsonify(all_authors=list_authors), 200
    except Exception as ex:
        logger.error("Error while issuing all authors: %s", str(ex))
        return jsonify({"error": f"message: {str(ex)}"}), 500


@app.route("/author/<int:id>", methods=["GET"])
def get_author_by_id(id: int):
    try:
        logger.info("Start get author by id")
        author = session.query(Authors).filter(Authors.id == id).one()
        logger.info("Successfully retrieved author with id: %s", id)
        return jsonify(author=author.to_json()), 200
    except Exception as ex:
        logger.error("Error searching author by id: %s", str(ex))
        return jsonify({"error": f"message: {str(ex)}"}), 500


@app.route("/author/name/<string:name>", methods=["GET"])
def get_author_by_name(name: str):
    try:
        logger.info("Start get author by name")
        authors = session.query(Authors).filter(Authors.name.like(f"%{name}%")).all()
        list_author = [author.to_json() for author in authors]
        logger.info("Author successfully found by name: %s", name)
        return jsonify(name=list_author), 200
    except Exception as ex:
        logger.error("Error searching author by name: %s", str(ex))
        return jsonify({"error": f"message: {str(ex)}"}), 500


@app.route("/author/<int:id>", methods=["DELETE"])
def delete_author_by_id(id: int):
    try:
        logger.info("Start delete author by id")
        author = session.query(Authors).filter(Authors.id == id).one_or_none()
        if not author:
            logger.info("Author not found: %s", id)
            return ({"message": "Автор не найден"}), 404
        session.delete(author)
        session.commit()
        logger.info("Author removed successfully: %s", id)
        return ({"message": "Автор успешно удален"}), 200
    except Exception as ex:
        session.rollback()
        logger.error("Error deleting author: %s", str(ex))
        return jsonify({"error": f"message: {str(ex)}"}), 500


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    check_exists = session.query(Authors).all()
    if not check_exists:
        insert_data(),
        give_my_book()
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(debug=True)
