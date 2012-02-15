from setuptools import setup
import os

readme = os.path.join(os.path.dirname(__file__), 'README.rst')
LONG_DESCRIPTION = open(readme).read()



setup(
    name             = 'tambo',
    description      = 'A command line object dispatcher',
    author           = 'Alfredo Deza',
    author_email     = 'alfredodeza [at] gmail.com',
    version          = '0.0.1',
    license          = "MIT",
    keywords         = "cli, command, command line, dispatcher, subcommands",
    install_requires = ['konira>=0.3.0'],
    long_description = LONG_DESCRIPTION
)
