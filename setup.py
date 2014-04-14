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
    version='0.1.0',
    packages=[
        'exclusivebooleanfield',
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
    cmdclass = {'test': Tox},
)
