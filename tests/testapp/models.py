from django.db import models

from exclusivebooleanfield.fields import ExclusiveBooleanField


class UnlimitedModel(models.Model):
    the_one = ExclusiveBooleanField(default=False)


class RelatedModel(models.Model):
    pass


class LimitedModel(models.Model):
    related = models.ForeignKey(RelatedModel, null=True)
    value = models.IntegerField(null=True)
    the_one = ExclusiveBooleanField(on=('related', 'value'), default=False)
