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

# Взаимодействие с Students
@app.route("/students", methods=["GET"])
def get_all_students():
    students = session.query(Students).all()
    list_students = []
    for student in students:
        list_students.append(student.to_json())
    return jsonify(all_students=list_students), 200

@app.route("/student/<int:id>", methods=["GET"])
def get_student_by_id(id: int):
    student = session.query(Students).filter(Students.id==id).one()
    return jsonify(student=student.to_json())

@app.route("/student/name/<string:name>", methods=["GET"])
def get_student_by_name(name:str):
    students = session.query(Students).filter(Students.name.like(f"%{name}%")).all()
    list_name = [student.to_json() for student in students]
    return jsonify(name=list_name)

# Взаимодействие с Books
@app.route("/books", methods=["GET"])
def get_all_books():
    books = session.query(Books).all()
    list_books = []
    for book in books:
        list_books.append(book.to_json())
    return jsonify(all_books=list_books)

@app.route("/book/<int:id>", methods=["GET"])
def get_book_by_id(id:int):
    book = session.query(Books).filter(Books.id==id).one()
    return jsonify(book=book.to_json())

@app.route("/book/name/<string:name>", methods=["GET"])
def get_book_by_name(name: str):
    books = session.query(Books).filter(Books.name.like(f"%{name}%")).all()
    list_book = [book.to_json() for book in books]
    return jsonify(name=list_book)

# Взаимодействие с Authors
@app.route("/authors", methods=["GET"])
def get_all_authors():
    authors = session.query(Authors).all()
    list_authors = []
    for author in authors:
        list_authors.append(author.to_json())
    return jsonify(all_authors=list_authors)

@app.route("/author/<int:id>", methods=["GET"])
def get_author_by_id(id:int):
    author = session.query(Authors).filter(Authors.id==id).one()
    return jsonify(author=author.to_json())

@app.route("/author/name/<string:name>", methods=["GET"])
def get_author_by_name(name: str):
    authors = session.query(Authors).filter(Authors.name.like(f"%{name}%")).all()
    list_author = [author.to_json() for author in authors]
    return jsonify(name=list_author)

if __name__ == "__main__":
    app.run(debug=True)
    check_exists = session.query(Authors).all()
    if not check_exists:
        insert_data(),
        give_my_book()
