import os
from setuptools import setup


# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = 'koopa',
    version = '0.0.1',
    author = 'Juan Hernandez',
    author_email = 'juan@xagnus.com',
    description = 'Library/Wrapper for l10n',
    license = 'BSD',
    keywords = 'l10n',
    packages=['l10n'],
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: BSD License',
    ],
    install_requires=['polib==1.1.0']
)
