from setuptools import setup

setup(
    name='projects.core',
    version='1.1.0',
    packages=['tests', 'tests.projects', 'tests.projects.core', 'tests.projects.core.db', 'tests.projects.core.io',
              'tests.projects.core.utils', 'tests.projects.core.objects', 'tests.projects.core.exceptions',
              'tests.projects.core.etuzon_http', 'projects', 'projects.core', 'projects.core.db',
              'projects.core.db.mongo_db', 'projects.core.io', 'projects.core.test', 'projects.core.utils',
              'projects.core.objects', 'projects.core.exceptions', 'projects.core.etuzon_http'],
    url='',
    license='',
    author='etuzon',
    author_email='eyal.tuzon.finance@gmail.com',
    description=''
)
