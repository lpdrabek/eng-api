import json
from datetime import datetime
from flask import render_template, request, abort, Response

from app import app, Session, db
from app.models import Author, Book
from app.return_codes import return_code


@app.route('/')
def main_page():
    return render_template("mainpage.html")


@app.route('/docs',
           strict_slashes=False)
def documentation():
    return render_template("docs.html", return_codes=return_code)


@app.route('/api/authors/',
           methods=['POST'], strict_slashes=False)
def autor_add():
    session = Session()
    full_name = ""
    birth_date = None
    death_date = None
    gender = None

    if len(request.json) == 0:
        return json.dumps(return_code[1]), 400

    if "full_name" in request.json:
        full_name = request.json["full_name"]
    else:
        return json.dumps(return_code[2]), 400

    if "birth_date" in request.json:
        birth_date = datetime.strptime(request.json["birth_date"],
                                       "%d-%m-%Y").date()
    if "death_date" in request.json:
        death_date = datetime.strptime(request.json["death_date"],
                                       "%d-%m-%Y").date()
    if "gender" in request.json:
        gender = request.json["gender"]

    new_author = Author(full_name=full_name, birth_date=birth_date,
                        death_date=death_date, gender=gender)
    if exists_in_db("full_name", full_name, "Author"):
        return json.dumps(return_code[3]), 409

    session.add(new_author)
    session.commit()

    rsp_dict = dict(return_code[0])
    rsp_dict["added"] = new_author.as_dict(show_id=True)
    rsp_dict = json.dumps(rsp_dict)

    rsp = Response(rsp_dict)
    rsp.headers.add("Location", "/api/authors/{}".format(new_author.id))

    session.close()
    return rsp, 201


@app.route('/api/authors/',
           methods=['GET'], strict_slashes=False)
def author_list():
    session = Session()
    query = session.query(Author)
    show_books = bool(int(request.args.get("show_books", 0)))
    show_id = bool(int(request.args.get("show_id", 0)))
    if "full_name" in request.args:
        query = query.filter(Author.full_name == request.args.get("full_name"))
    if "birth_date" in request.args:
        query = query.filter(Author.birth_date == request.args.get("birth_date"))
    if "death_date" in request.args:
        query = query.filter(Author.death_date == request.args.get("death_date"))
    if "gender" in request.args:
        query = query.filter(Author.gender == request.args.get("gender"))

    rsp = [author.as_dict(show_id, show_books) for author in query]
    session.close()
    return json.dumps(rsp)


@app.route('/api/authors/<int:author_id>',
           methods=['GET'], strict_slashes=False)
def author_list_by_id(author_id):
    session = Session()
    query = session.query(Author)
    show_books = True
    show_id = False

    if not exists_in_db("id", author_id, "Author"):
        return json.dumps(return_code[4]), 404

    query = query.filter(Author.id == author_id)

    if request.args.get("show_books") == 0:
        show_books = False
    if request.args.get("show_id") == 1:
        show_id = True
    rsp = [author.as_dict(show_id, show_books) for author in query]

    session.close()
    return json.dumps(rsp)


@app.route('/api/authors/<int:author_id>',
           methods=["PUT", "PATCH"], strict_slashes=False)
def author_update(author_id):
    session = Session()
    to_update = {}

    if "full_name" in request.json:
        to_update["full_name"] = request.json["full_name"]
    if "birth_date" in request.json:
        to_update["birth_date"] = request.json["birth_date"]
    if "death_date" in request.json:
        to_update["death_date"] = request.jsoni["death_date"]
    if "gender" in request.json:
        to_update["gender"] = request.json["gender"]

    if len(to_update) == 0:
        return json.dumps(return_code[1]), 204

    author = session.query(Author).filter(Author.id == author_id).first()

    if not author:
        return json.dumps(return_code[4]), 404

    for parameter, value in to_update.items():
        setattr(author, parameter, value)

    session.add(author)
    session.commit()

    rsp_dict = dict(return_code[0])
    rsp_dict["updated"] = author.as_dict(show_id=True)
    rsp_dict = json.dumps(rsp_dict)

    rsp = Response(rsp_dict)

    session.close()
    return rsp, 200


@app.route('/api/authors/<int:author_id>',
           methods=["DELETE"], strict_slashes=False)
def author_delete(author_id):
    session = Session()
    if not exists_in_db("id", author_id, "Author"):
        return json.dumps(return_code[4]), 404

    to_delete = session.query(Author).filter(Author.id == author_id).first()

    session.delete(to_delete)
    session.commit()

    rsp_dict = dict(return_code[0])
    rsp_dict["deleted"] = to_delete.as_dict(show_id=True, show_books=True)
    rsp_dict = json.dumps(rsp_dict)

    rsp = Response(rsp_dict)

    session.close()
    return rsp, 200


@app.route('/api/authors',
           methods=['PUT', 'PATCH', 'DELETE'], strict_slashes=False)
def author_list_404():
    abort(404)


@app.route('/api/books/',
           methods=['POST'], strict_slashes=False)
def book_add():
    session = Session()
    authorid = None
    title = None
    isbn = None
    read = 0

    if len(request.json) == 0:
        return json.dumps(return_code[1]), 400

    if "title" in request.json:
        title = request.json["title"]
    else:
        return json.dumps(return_code[2]), 400

    if "author_id" in request.json:
        authorid = request.json["author_id"]
        if not exists_in_db("id", authorid, "Author"):
            return json.dumps(return_code[5]) ,400
    else:
        return json.dumps(return_code[2]), 400

    if "isbn" in request.json:
        isbn = request.json["isbn"]
    if "read" in request.json:
        read = request.json["read"]

    new_book = Book(authorid, title,
                    isbn=isbn, book_read=read)

    if exists_in_db("title", title, "Book"):
        return json.dumps(return_code[3]), 409
    if exists_in_db("isbn", isbn, "Book"):
        return json.dumps(return_code[3]), 409

    session.add(new_book)
    session.commit()

    rsp_dict = dict(return_code[0])
    rsp_dict["added"] = new_book.as_dict(show_id=True)
    rsp_dict = json.dumps(rsp_dict)

    rsp = Response(rsp_dict)
    rsp.headers.add("Location", "/api/books/{}".format(new_book.id))

    session.close()
    return rsp, 201


@app.route('/api/books',
           methods=['GET'], strict_slashes=False)
def book_list():
    session = Session()
    query = session.query(Book)
    show_author = bool(int(request.args.get("show_author", 0)))
    show_id = bool(int(request.args.get("show_id", 0)))
    if "title" in request.args:
        query = query.filter(Book.title == request.args.get("title"))
    if "isbn" in request.args:
        query = query.filter(Book.isbn == request.args.get("isbn"))
    if "book_read" in request.args:
        query = query.filter(Book.book_read == request.args.get("book_read"))

    rsp = [book.as_dict(show_id, show_author) for book in query]
    session.close()
    return json.dumps(rsp), 200


@app.route('/api/books/<int:book_id>',
           methods=['GET'], strict_slashes=False)
def book_list_by_id(book_id):
    session = Session()
    query = session.query(Book).filter(Book.id == book_id)
    show_author = False
    show_id = False

    if not exists_in_db("id", book_id, "Book"):
        return json.dumps(return_code[4]), 404

    if request.args.get("show_author") == "1":
        show_author = True
    if request.args.get("show_id") == "1":
        show_id = True

    rsp = [book.as_dict(show_id, show_author) for book in query]
    session.close()
    return json.dumps(rsp), 200


@app.route('/api/books/<int:book_id>',
           methods=["PUT", "PATCH"], strict_slashes=False)
def book_update(book_id):
    session = Session()
    to_update = {}

    if "title" in request.json:
        to_update["title"] = request.json["title"]
    if "isbn" in request.json:
        to_update["isbn"] = request.json["isbn"]
    if "book_read" in request.json:
        to_update["book_read"] = request.json["book_read"]
    if "author_id" in request.json:
        to_update["authorid"] = request.json["author_id"]
        if not exists_in_db("id", to_update["author_id"], "Author"):
            return json.dumps(return_code[5]), 404

    if len(to_update) == 0:
        return json.dumps(return_code[1]),204

    book = session.query(Book).filter(Book.id == book_id).first()

    if not book:
        return json.dumps(return_code[4]), 404

    for parameter, value in to_update.items():
        setattr(book, parameter, value)

    session.add(book)
    session.commit()

    rsp_dict = dict(return_code[0])
    rsp_dict["updated"] = book.as_dict(show_id=True)
    rsp_dict = json.dumps(rsp_dict)

    rsp = Response(rsp_dict)

    session.close()
    return rsp, 200


@app.route('/api/books/<int:book_id>',
           methods=['DELETE'], strict_slashes=False)
def book_delete(book_id):
    session = Session()
    if not exists_in_db("id", book_id, "Book"):
        return json.dumps(return_code[4]), 404

    to_delete = session.query(Book).filter(Book.id == book_id).first()

    session.delete(to_delete)
    session.commit()

    rsp_dict = dict(return_code[0])
    rsp_dict["deleted"] = to_delete.as_dict(show_id=True)
    rsp_dict = json.dumps(rsp_dict)

    rsp = Response(rsp_dict)

    session.close()
    return rsp, 200


@app.route('/api/books',
           methods=['PUT', 'PATCH', 'DELETE'], strict_slashes=False)
def book_list_404():
    abort(404)


def exists_in_db(var, value, obj):
    session = Session()
    query = ""
    if obj == "Author":
        query = session.query(Author)
        if var == "full_name":
            query = query.filter(Author.full_name == value).first()
        if var == "id":
            query = query.filter(Author.id == value).first()
    elif obj == "Book":
        query = session.query(Book)
        if var == "title":
            query = query.filter(Book.title == value).first()
        if var == "isbn" and value:
            query = query.filter(Book.isbn == value).first()
        elif not value:
            return False
        if var == "id":
            query = query.filter(Book.id == value).first()
    session.close()
    if query:
        return True
    return False
