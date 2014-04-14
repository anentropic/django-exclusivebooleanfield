django-exclusivebooleanfield
============================

Provides an `ExcluveBooleanField` which is a boolean (db) field where only one row in the table (or optionally, a subset of table based on value of other fields) is `True` and all the other rows are `False.

Tested on Django 1.3 thru 1.7, to run tests checkout the project and `python setup.py test`
