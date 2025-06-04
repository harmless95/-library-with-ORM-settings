from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from main import Base

class Students(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(100), nullable=False)

    receiving_student = relationship("ReceivingBooks", back_populates="student")


class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    id_author = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", backref=backref("books",
                                                    cascade="all, "
                                                            "delete-orphan",
                                                    lazy="select"))
    receiving_book = relationship("", back_populates="book")

class Authors(Base):
    __table__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)

class ReceivingBooks(Base):
    __tablename__ = "receiving_books"

    student = relationship("Students", back_populates="receiving_student")
    book = relationship("Books", back_populates="receiving_book")

