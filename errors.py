"""Errors the services raise. The routes turn them into HTTP status codes."""


class LibraryError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class InvalidRequest(LibraryError):
    """The input is missing or badly formed (HTTP 400)."""


class NotFound(LibraryError):
    """The book, member or loan doesn't exist (HTTP 404)."""


class Conflict(LibraryError):
    """A library rule blocks the action (HTTP 409)."""


def require(item, message):
    """Return item, or raise NotFound if it is None."""
    if item is None:
        raise NotFound(message)
    return item
