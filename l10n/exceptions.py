"""Exceptions for goomba.translations."""


class KeyDoesNotExistException(Exception):
    """Raised if the given translation key was not found."""


class DirectoryDoesNotExistException(Exception):
    """Raised if the given l10n directory does not exist."""


class FileDoesNotExistException(Exception):
    """Raised if the given file does not exist."""
