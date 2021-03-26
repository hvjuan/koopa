"""Tests for koopa.translations."""

import pytest

from koopa import exceptions as koopa_exceptions
from koopa import translations


_BASE_TRANSLATIONS = 'tests/mocked_translations'


class TestTranslate:
    
    def test_translation__polish(self):
        translate = translations.Translate(_BASE_TRANSLATIONS)
        translated_string = translate.translate(
            'first_level.mockedTestId', 'pl-PL')
        assert 'This is the Polish mocked translation' == translated_string

    def test_translation__german(self):
        translate = translations.Translate(_BASE_TRANSLATIONS)
        translated_string = translate.translate(
            'first_level.mockedTestId', 'de-DE')
        assert 'This is the German mocked translation' == translated_string

    def test_translation__uk_english(self):
        translate = translations.Translate(_BASE_TRANSLATIONS)
        translated_string = translate.translate(
            'first_level.mockedTestId', 'en-GB')
        assert ('This is the British '
                'English mocked translation') == translated_string

    def test_translation__default(self):
        translate = translations.Translate(_BASE_TRANSLATIONS)
        # Not passing a locale should fall back to base english.
        translated_string = translate.translate('first_level.mockedTestId')
        assert 'This is the Base English Translation' == translated_string

    def test_translation__fallback(self):
        translate = translations.Translate(_BASE_TRANSLATIONS)
        # If an uknown key is given that doesn't exist, is very likely that 
        # the specific translation may not be ready, so we must always fall
        # back to the base.
        translated_string = translate.translate(
            'first_level.mockedTestId', 'xx-XX')
        assert 'This is the Base English Translation' == translated_string

    def test_translation__raise_key_does_not_exist(self):
        translate = translations.Translate(_BASE_TRANSLATIONS)
        with pytest.raises(koopa_exceptions.KeyDoesNotExistException) as e:
            translate.translate('first_level.thisKeyDoesNotExist', 'en-GB')
        assert ('The translation key '
                'thisKeyDoesNotExist was not found.') == e.value.args[0]

    def test_translation__default(self):
        translate = translations.Translate(_BASE_TRANSLATIONS)
        # Not passing a locale should fall back to base english.
        translated_string = translate.translate('first_level.mockedTestId')
        assert 'This is the Base English Translation' == translated_string
