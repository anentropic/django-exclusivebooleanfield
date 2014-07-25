django-exclusivebooleanfield
============================

[![Build Status](https://travis-ci.org/anentropic/django-exclusivebooleanfield.svg?branch=master)](https://travis-ci.org/anentropic/django-exclusivebooleanfield)
[![Latest PyPI version](https://pypip.in/version/django-exclusivebooleanfield/badge.svg)](https://pypip.in/version/django-exclusivebooleanfield/badge.svg)
[![Supported Python versions](https://pypip.in/py_versions/django-exclusivebooleanfield/badge.svg)](https://pypip.in/py_versions/django-exclusivebooleanfield/badge.svg)

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

Tested on Django 1.3 thru 1.7, to run tests checkout the project and `python setup.py test`
