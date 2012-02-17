import sys
import os

readme = os.path.join(os.path.dirname(__file__), 'README.rst')
LONG_DESCRIPTION = open(readme).read()


# Python3 needs this
if sys.version < '3':
    from setuptools import setup
    extra = dict()
else:
    import distribute_setup
    distribute_setup.use_setuptools()
    from setuptools import setup
    extra = {'use_2to3':True}


setup(
    name             = 'tambo',
    description      = 'A command line object dispatcher',
    packages         = ['tambo'],
    author           = 'Alfredo Deza',
    author_email     = 'alfredodeza [at] gmail.com',
    version          = '0.0.1',
    license          = "MIT",
    zip_safe         = False,
    keywords         = "cli, command, command line, dispatcher, subcommands",
    install_requires = ['konira>=0.3.0', 'mock', 'tox'],
    long_description = LONG_DESCRIPTION,
    **extra
)
