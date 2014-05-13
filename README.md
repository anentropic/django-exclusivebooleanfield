django-exclusivebooleanfield
============================

[![Build Status](https://travis-ci.org/anentropic/django-exclusivebooleanfield.svg?branch=master)](https://travis-ci.org/anentropic/django-exclusivebooleanfield)

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
```

Tested on Django 1.3 thru 1.7, to run tests checkout the project and `python setup.py test`
