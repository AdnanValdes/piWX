try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'An aviation weather streaming service.',
    'author': 'Adnan Valdes',
    'author_email': 'adravaldes@protonmail.com',
    'version': '0.1',
    'install_requires': ['avwx-engine'],
    'name': 'piWX',
    'license': 'MIT',
    'platforms': ['NT', 'Linux']

}

setup(**config)