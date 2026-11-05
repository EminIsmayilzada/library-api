from flask import Blueprint, jsonify, request

from serializers import book_to_dict
from services import books as service

bp = Blueprint("books", __name__)


@bp.get("/books")
def list_books():
    only_available = request.args.get("available") == "true"
    return jsonify([book_to_dict(book) for book in service.list_books(only_available)])


@bp.get("/books/<int:book_id>")
def get_book(book_id):
    return jsonify(book_to_dict(service.get_book(book_id)))


@bp.post("/books")
def create_book():
    data = request.get_json(silent=True) or {}
    return jsonify(book_to_dict(service.add_book(data))), 201


@bp.delete("/books/<int:book_id>")
def delete_book(book_id):
    service.remove_book(book_id)
    return "", 204
