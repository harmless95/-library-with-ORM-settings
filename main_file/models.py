import re
from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Boolean, Float
from sqlalchemy.orm import relationship, backref, validates

from .session_file import session
from .base_file import Base


class Students(Base):
    """Обьект студента"""
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(100), nullable=False)
    scholarship = Column(Boolean, nullable=False)
    average_score = Column(Float, nullable=False)

    receiving_student = relationship("ReceivingBooks", back_populates="student")

    def to_json(self):
        return {s.name: getattr(self, s.name) for s in self.__table__.columns}

    @validates("email")
    def validate_email(self, key, address):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, address):
            raise ValueError(f"Некорректная электроная почта: {address}")
        return address

    @validates("phone")
    def validate_phone(self, key, number):
        pattern = r'^\+7\d{7,}$'
        if not re.match(pattern, number):
            raise ValueError(f"Некорректный номер телефона: {number}")
        return number


class Books(Base):
    """Обьект книги"""
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    id_author = Column(Integer, ForeignKey("authors.id"))
    receiving_book = relationship("ReceivingBooks", back_populates="book")
    author = relationship("Authors", back_populates="books")

    def to_json(self):
        return {book.name: getattr(self, book.name) for book in self.__table__.columns}

class Authors(Base):
    """Обьект автора"""
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    books = relationship("Books", back_populates="author", cascade="all, delete-orphan", lazy="select")

    def __repr__(self):
        return f"Имя: {self.name}, Фамилия: {self.surname}"

    def to_json(self):
        return {i.name: getattr(self, i.name) for i in self.__table__.columns}

class ReceivingBooks(Base):
    """Выдача книг"""
    __tablename__ = "receiving_books"

    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey("books.id"), nullable=False)
    id_student = Column(Integer, ForeignKey("students.id"), nullable=False)
    date_issue = Column(DateTime, default=datetime.now())
    date_return = Column(DateTime, nullable=True)

    student = relationship("Students", back_populates="receiving_student")
    book = relationship("Books", back_populates="receiving_book")

    def __repr__(self):
        return (f"Книга: {self.id_book},"
                f"Студент: {self.id_student},"
                f"Дата выдачи: {self.date_issue},"
                f"Дата возврата: {self.date_return},"
                f"Кол-во дней, который держал/держит читатель: {self.count_date_book()}")

    def count_date_book(self):
        if self.date_return:
            return (self.date_return - self.date_issue).days
        else:
            return (datetime.now() - self.date_issue).days

    def to_json(self):
        return {"id": self.id,
                "id_book": self.id_book,
                "id_student": self.id_student,
                "date_issue": self.date_issue,
                "date_return": self.date_return,
                "count_date_book": self.count_date_book()}

    @classmethod
    def get_list_students(cls):
        students = session.query(Students).filter(Students.scholarship == True).all()
        students_list = []
        for student in students:
            students_list.append(student.to_json())
        return students_list

    @classmethod
    def get_list_students_score(cls, number):
        students = session.query(Students).filter(Students.average_score > number).all()
        students_list = []
        for student in students:
            students_list.append(student.to_json())
        return students_list

