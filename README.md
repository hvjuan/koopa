# Project Koopa: l10n library.

Simple library/wrapper to easily process .po files.

### Flask Usage.

- Create our translations directory in our project root folder, ie: 
```bash
mkdir translations
```
- Create subdirectories to categorize modules/sections. This module will have 
  all the `messages.po` files
```bash
mkdir translations/my_module
```

- Create base translation file. In `translations/my_module` create
  `messages.po` and add your initial strings:

```
msgid "myMessageKey"
msgstr "This is the message I'll translate"
```

at this point, your system should be ready for your l10n process.

- Create webserver object, ie: flask's `app.py`:
```python

from l10n import translations

# Translate takes two arguments, base_path containing the .po files
# and optionally, file_name for the main .po name, defaulting to 'messages'.

_L10N_DIR = 'translations'
...
app = flask.Flask(__name__)
...
# Create an instance and add it to the local flask object.
app.l10n = translations.Translate(_L10N_DIR)

```
- Then, on every module/blueprint, let's use this module
```python
from flask import current_app

...
@my_blueprint.route('/localized/<locale>')
def localized(locale: str):
    # Here we'll access the l10n instance and request the key we want.
    # The translate method takes two arguments, complete path after the 
    # base path and the translation key, since we configured the instance with
    # 'translations/my_module', to get to tjhe key, we need to use dotted
    # notation ending with the key. This assumes that your l10n process already
    # processed your base .po file. If a given locale was not found, defaults
    # to messages.po.
    localized_string = current_app.l10n.translate(
        'my_module.myMessageKey', 'de-DE')
    return f'The localized str is: {localized_string}'
```
