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
        file_name: default file name. Can be added at instantiation time in case
            is other than messages.po/messages.*.po.
    """

    def __init__(self, base_path: str, file_name: str = _MESSAGES):
        if not os.path.isdir(base_path):
            raise koopa_exceptions.DirectoryDoesNotExistException(
                f'Path {base_path} was not found')
        self.base_path = base_path
        self.file_name = file_name

    def translate(self, key_path: str, locale='en-US'):
        """Main translation method.

        Args:
            key_path: path to the translation key to use using dot notation.
            locale: locale code to be using.
        Returns:
            Translated or default string.
        """
        *key_path, translation_key = key_path.split('.')
        full_path = self._build_route(key_path, locale)
        return self._get_key(full_path, translation_key, locale)

    def _get_key(self, full_path: str, translation_key: str, locale: str):
        """Gets translation key from localized files.

        Args:
            full_path: complete path to the corresponding .po file.
            translation_key: translation key containing the localized text.
        Returns:
            Translated or default string.
        Raises:
            koopa_exceptions.KeyDoesNotExistException: raised if the given
                key was not found.
        """
        for entry in polib.pofile(full_path):
            if translation_key == entry.msgid:
                return entry.msgstr

        raise koopa_exceptions.KeyDoesNotExistException(
            f'The translation key {translation_key} was not found.')

    def _build_route(self, key_path: List[str], locale: str) -> str:
        """Builds and returns route to the .po translation file.
        
        Builds it from the object path, self.file_name and locale.

        Falls back to base locale if default hasn't changed or it wasn't
        found on the file system. Fail silently but check again that at least
        the base file exists, ie: messages.po

        Args:
            key_path: List of strings with the local path to the translation file.
            locale: specific locale to get data from.
        Returns: 
            String with complete path to the .po file.
        Raises:
            koopa_exceptions.FileDoesNotExistException: raised if the final default file
                path created does not exist.
        """
        key_path = '/'.join(key_path)

        if locale is not _BASE_LOCALE:
            full_path = (
                f'{self.base_path}/{key_path}/{self.file_name}.{locale}.po')
            # Check if file exists, otherwise fall back to _BASE_LOCALE.
            if os.path.isfile(full_path):
                return full_path
        # Fallback.
        default = f'{self.base_path}/{key_path}/messages.po'
        if not os.path.isfile(default):
            raise koopa_exceptions.FileDoesNotExistException(
                f'{default} was not found.')
        return default
