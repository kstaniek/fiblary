from setuptools import setup, find_packages

find_packages('jsonpatch')


setup(
    name = 'Fiblary',
    description = 'Home Center 2 API Python Library',
    author = 'Klaudiusz Staniek',
    author_email = 'klaudiusz@staniek.name',

    packages = [
        'jsonpatch',
        'netaddr',
        'prettytable',
        'python-dateutil',
        'requests',
        'sox',
        'Sphinx'
        ],
)

