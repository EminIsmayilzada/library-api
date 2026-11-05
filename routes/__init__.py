"""The HTTP layer: URLs, request parsing, JSON responses and status codes."""
from flask import jsonify

from errors import Conflict, InvalidRequest, LibraryError, NotFound

from . import books, loans, members, reports

STATUS_CODES = {InvalidRequest: 400, NotFound: 404, Conflict: 409}


def register_routes(app):
    for module in (books, members, loans, reports):
        app.register_blueprint(module.bp)

    @app.errorhandler(LibraryError)
    def handle_library_error(error):
        return jsonify({"error": error.message}), STATUS_CODES.get(type(error), 400)
