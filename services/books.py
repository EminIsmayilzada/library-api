import repository as repo
from db import connection
from errors import Conflict, InvalidRequest, require
from validation import is_valid_isbn


def list_books(only_available=False):
    with connection() as conn:
        return repo.list_books(conn, only_available)


def get_book(book_id):
    with connection() as conn:
        return require(repo.find_book(conn, book_id), "book not found")


def add_book(data):
    if not data.get("title") or not data.get("author"):
        raise InvalidRequest("title and author are required")
    if not is_valid_isbn(data.get("isbn")):
        raise InvalidRequest("invalid isbn")
    with connection() as conn:
        book_id = repo.insert_book(conn, data["title"], data["author"], data["isbn"])
        return repo.find_book(conn, book_id)


def remove_book(book_id):
    with connection() as conn:
        book = require(repo.find_book(conn, book_id), "book not found")
        if not book["available"]:
            raise Conflict("book is on loan")
        repo.delete_book(conn, book_id)
