from flask import Flask, jsonify

from main_file.base_file import Base
from main_file.session_file import engine, session
from main_file.models import Students, Authors, Books
from insert_db_file import insert_data
from give_db_file import give_my_book


app = Flask(__name__)

@app.before_request
def base_metadata():
    Base.metadata.create_all(engine)

@app.route("/students", methods=["GET"])
def get_all_students():
    students = session.query(Students).all()
    list_students = []
    for student in students:
        list_students.append(student.to_json())
    return jsonify(list_students=list_students), 200

@app.route("/books", methods=["GET"])
def get_all_books():
    books = session.query(Books).all()
    list_books = []
    for book in books:
        list_books.append(book.to_json())
    return jsonify(list_books=list_books)


if __name__ == "__main__":
    app.run(debug=True)
    check_exists = session.query(Authors).all()
    if not check_exists:
        insert_data(),
        give_my_book()
