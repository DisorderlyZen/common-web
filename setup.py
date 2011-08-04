from distutils.core import setup
from dzen import __version__

setup(
        name='DZ Common Web',
        description='Common apps for creating DZ websites',
        version=__version__,
        author='Craig Slusher',
        author_email='craig@disorderlyzen.com',
        packages=['dzen']
        )
