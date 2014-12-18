import sys

from distutils.core import setup
from setuptools.command.test import test as TestCommand


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        errno = tox.cmdline(self.test_args)
        sys.exit(errno)


setup(
    name='django-exclusivebooleanfield',
    description="Provides an `ExcluveBooleanField` which is a boolean (db) "
                "field where only one row in the table (or optionally, a "
                "subset of table based on value of other fields) is `True` "
                "and all the other rows are `False.",
    version='0.3.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        # 'Framework :: Django :: 1.3',
        # 'Framework :: Django :: 1.4',
        # 'Framework :: Django :: 1.5',
        # 'Framework :: Django :: 1.6',
        # 'Framework :: Django :: 1.7',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
    packages=[
        'exclusivebooleanfield',
    ],
    install_requires=[
        'six>=1.8.0'
    ],
    license='MIT',
    long_description=open('pypi.rst').read(),
    author="Anentropic",
    author_email="ego@anentropic.com",
    url="https://github.com/anentropic/django-exclusivebooleanfield",
    tests_require=[
        'tox>=1.7.1',
        'pytest-django>=1.7.1',
    ],
    cmdclass={'test': Tox},
)
