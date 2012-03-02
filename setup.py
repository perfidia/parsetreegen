import os
from setuptools import setup, find_packages

PACKAGE_DIR = 'src'

def read(file_name):
	return open(os.path.join(os.path.dirname(__file__), file_name)).read()

setup(
	name = "parsetreegen",
	version = '0.0.1',
	author = read("AUTHORS"),
	keywords = "parse tree generator",
	url = "https://github.com/perfidia/parsetreegen",
	package_dir = {'': PACKAGE_DIR},
	long_description = read("README.md"),
	packages = find_packages(PACKAGE_DIR, exclude=['ez_setup', 'examples', 'tests']),
	zip_safe = False,
)

