django-exclusivebooleanfield
============================

[![Build Status](https://travis-ci.org/anentropic/django-exclusivebooleanfield.svg?branch=master)](https://travis-ci.org/anentropic/django-exclusivebooleanfield)
[![Latest PyPI version](https://badge.fury.io/py/django-exclusivebooleanfield.svg)](https://pypi.python.org/pypi/django-conditional-aggregates/)  
![Tested for: Python 2.6](https://img.shields.io/badge/Python%202.6--brightgreen.svg)
![Tested for: Python 2.7](https://img.shields.io/badge/Python%202.7--brightgreen.svg)
![Tested for: Python 3.4](https://img.shields.io/badge/Python%203.4--brightgreen.svg)  
![Tested for: Django 1.3](https://img.shields.io/badge/Django%201.3--brightgreen.svg)
![Tested for: Django 1.4](https://img.shields.io/badge/Django%201.4--brightgreen.svg)
![Tested for: Django 1.5](https://img.shields.io/badge/Django%201.5--brightgreen.svg)
![Tested for: Django 1.6](https://img.shields.io/badge/Django%201.6--brightgreen.svg)
![Tested for: Django 1.7](https://img.shields.io/badge/Django%201.7--brightgreen.svg)
![Tested for: Django 1.8](https://img.shields.io/badge/Django%201.8--brightgreen.svg)


Provides an `ExclusiveBooleanField` which is a boolean (db) field where only one row in the table (or optionally, a subset of table based on value of other fields) is `True` and all the other rows are `False`.

Usage:
```python
from django.db import models

from exclusivebooleanfield.fields import ExclusiveBooleanField


class MyModel(models.Model):
    the_one = ExclusiveBooleanField()


class MyModel(models.Model):
    field_1 = ForeignKey()
    field_2 = CharField()
    the_one = ExclusiveBooleanField(on=('field_1', 'field_2'))
    # `on` is a bit like a unique constraint, value of field
    # is only exclusive for rows with same value of the on fields


class MyOtherModel(models.Model):
    field_1 = CharField()
    the_one = ExclusiveBooleanField(on='field_1')
    # if `on` is just a single field you don't have to wrap in a tuple
```

Tested on Django 1.3 thru 1.8, to run tests checkout the project and `python setup.py test`
