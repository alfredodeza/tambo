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
    version          = '0.0.3',
    license          = "MIT",
    zip_safe         = False,
    keywords         = "cli, command, command line, dispatcher, subcommands",
    long_description = LONG_DESCRIPTION,
    classifiers      = [
                        'Development Status :: 4 - Beta',
                        'Intended Audience :: Developers',
                        'License :: OSI Approved :: MIT License',
                        'Topic :: Software Development :: Build Tools',
                        'Topic :: Software Development :: Libraries',
                        'Topic :: Software Development :: Testing',
                        'Topic :: Utilities',
                        'Operating System :: MacOS :: MacOS X',
                        'Operating System :: Microsoft :: Windows',
                        'Operating System :: POSIX',
                        'Programming Language :: Python :: 2.5',
                        'Programming Language :: Python :: 2.6',
                        'Programming Language :: Python :: 2.7',
                        'Programming Language :: Python :: 3.0',
                        'Programming Language :: Python :: 3.1',
                        'Programming Language :: Python :: 3.2',
                        'Programming Language :: Python :: Implementation :: PyPy'
                      ],
    **extra
)
