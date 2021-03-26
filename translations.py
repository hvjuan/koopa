"""Main translation mode."""

import os
from typing import List

import polib

from koopa import exceptions as koopa_exceptions


# TODO(juan) raise exception if there's not at least one app.desc

_BASE_LOCALE = 'en-US'
# TODO(juan) messages is a filename, let's customize it.
_MESSAGES = 'messages'


class Translate:
    """Main translation class.

    This module will process .po files and will fall back to _MESSAGES.po
    if the given key does not exist.

    Properties:
        base_path: project path to base translations document.
    """

    def __init__(self, base_path: str):
        self.base_path = base_path
        # TODO(juan) Check that base exists at instance time.

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
            full_path = f'{self.base_path}/{key_path}/{_MESSAGES}.{locale}.po'
            # Check if file exists, otherwise fall back to _BASE_LOCALE.
            if os.path.isfile(full_path):
                return full_path
        # Fall back to base locale if default hasn't changed or it wasn't
        # found on the file system. Fail silently.
        return f'{self.base_path}/{key_path}/messages.po'
