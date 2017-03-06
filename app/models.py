import datetime
from app import db
from sqlalchemy.orm import relationship


class Book(db.Model):
    __tablename__ = "book"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    authorid = db.Column(db.Integer, db.ForeignKey('author.id'))
    title = db.Column(db.String(256))
    isbn = db.Column(db.String(15))
    book_read = db.Column(db.String(1))

    author = relationship("Author", back_populates="books")

    def __init__(self, authorid, title, isbn=None, book_read=0):
        self.authorid = authorid
        self.title = title
        self.isbn = isbn
        self.book_read = book_read

    def as_dict(self, show_id=False, show_author=False):
        rsp = {"title": self.title,
               "isbn": self.isbn,
               "book_read": self.book_read}

        if show_author:
            rsp["author"] = self.author.as_dict()
        if show_id:
            rsp["id"] = self.id

        return rsp


class Author(db.Model):
    __tablename__ = "author"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.Text())
    birth_date = db.Column(db.Date)
    death_date = db.Column(db.Date)
    gender = db.Column(db.String(1))

    books = relationship("Book", back_populates="author", cascade="delete")

    def __init__(self, full_name, birth_date=None, death_date=None, gender=None):
        self.full_name = full_name
        self.gender = gender

        if isinstance(birth_date, str):
            self.birth_date = datetime.datetime.strptime(birth_date, "%d-%m-%Y")
        else:
            self.birth_date = birth_date
        if isinstance(death_date, str):
            self.death_date = datetime.datetime.strptime(death_date, "%d-%m-%Y")
        else:
            self.death_date = death_date

    def as_dict(self, show_id=False, show_books=False):
        rsp = {"name": self.full_name,
               "birth_date": str(self.birth_date) if self.birth_date else None,
               "death_date": str(self.death_date) if self.birth_date else None,
               "gender": self.gender}

        if show_books:
            rsp["books"] = [book.as_dict() for book in self.books]
        if show_id:
            rsp["id"] = self.id

        return rsp
