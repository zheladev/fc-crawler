import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

requires = [
    'scrapy==1.6.0',
    'SQLAlchemy==1.3.3',
    'psycopg2-binary==2.7.6.1',
]

tests_require = [
    'freezegun==0.3.11'
]

quality_require = [
    'flake8==3.7.*',
]

scripts = [
    'initdb = '
    'fc_scrapper.scripts.initdb:main',
    'crawl_general = '
    'fc_scrapper:main',
]

setup(
    name='fc-crawler',
    version='0.1.0',
    description='forocoches subforum/thread crawler',
    long_description=README + '\n',
    classifiers=[
        'Programming Language :: Python',
    ],
    author='zheladev',
    author_email='zheladev@gmail.com',
    url='',
    keywords='crawler scrapy forocoches roto2',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
        'quality': quality_require,
    },
    install_requires=requires,
    entry_points={
        'console_scripts': scripts
    },
)
