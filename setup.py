from setuptools import setup, find_packages
from projects.core import __version__

with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name='projects_core',
    version=__version__,
    packages=find_packages(),
    url='',
    license='',
    author='etuzon',
    author_email='eyal.tuzon.dev@gmail.com',
    description='',
    install_requires=requirements
)
