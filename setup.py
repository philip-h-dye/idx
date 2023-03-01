from setuptools import setup, find_packages
from distutils.util import convert_path

version_ns = {}
with open(convert_path('idx/version.py')) as f:
    exec(f.read(), version_ns)

setup(
    name = 'idx',
    version = version_ns['__version__'],
    description = r"Enhanced 'id' with vertical listing, JSON and YAML outputs.",
    author = 'Philip H. Dye',
    author_email = 'philip@phd-solutions.com',
    packages = find_packages(),
    requires = ['docopt', 'unittest'],
    # install_requires = [],
    #
    # /usr/lib/python3.9/distutils/dist.py:274: UserWarning: Unknown distribution option: 'test_requires'
    # test_requires = ['unittest'],
    #
    entry_points = '''
        [console_scripts]
            idx = idx:main
	'''
)
