"""Main translation mode."""

import os
from typing import List

import polib

from l10n import exceptions as koopa_exceptions


_BASE_LOCALE = 'en-US'
_MESSAGES = 'messages'


class Translate:
    """Main translation class.

    This module will process .po files and will fall back to _MESSAGES.po
    if the given key does not exist.

    Properties:
        base_path: project path to base translations document.
    """

    def __init__(self, base_path: str, file_name: str = _MESSAGES):
        if not os.path.isdir(base_path):
            raise koopa_exceptions.DirectoryDoesNotExistException(
                f'Path {base_path} was not found')
        self.base_path = base_path
        self.file_name = file_name

    def translate(self, key_path: str, locale='en-US'):
        *key_path, translation_key = key_path.split('.')
        full_path = self._build_route(key_path, locale)
        return self._get_key(full_path, translation_key, locale)

    def _get_key(self, full_path: str, translation_key: str, locale: str):
        # TODO(juan) what happens when we give it a wrong file?
        for entry in polib.pofile(full_path):
            if translation_key == entry.msgid:
                return entry.msgstr

        raise koopa_exceptions.KeyDoesNotExistException(
            f'The translation key {translation_key} was not found.')

    def _build_route(self, key_path: List[str], locale: str) -> str:
        key_path = '/'.join(key_path)

        if locale is not _BASE_LOCALE:
            full_path = (
                f'{self.base_path}/{key_path}/{self.file_name}.{locale}.po')
            # Check if file exists, otherwise fall back to _BASE_LOCALE.
            if os.path.isfile(full_path):
                return full_path
        # Fall back to base locale if default hasn't changed or it wasn't
        # found on the file system. Fail silently but check again that at least
        # the base file exists, ie: messages.po
        default = f'{self.base_path}/{key_path}/messages.po'
        if not os.path.isfile(default):
            raise koopa_exceptions.FileDoesNotExistException(
                f'{default} was not found.')
        return default
