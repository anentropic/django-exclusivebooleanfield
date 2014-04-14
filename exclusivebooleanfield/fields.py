from django.db import models, transaction
from django.db.models import Q


class ExclusiveBooleanField(models.BooleanField):
    """
    Usage:

    class MyModel(models.Model):
        the_one = ExclusiveBooleanField()


    class MyModel(models.Model):
        field_1 = ForeignKey()
        field_2 = CharField()
        the_one = ExclusiveBooleanField(on=('field_1', 'field_2'))
        # `on` is a bit like a unique constraint, value of field
        # is only exclusive for rows with same value of the on fields
    """
    def __init__(self, on=None, *args, **kwargs):
        self._on_fields = on or ()
        super(ExclusiveBooleanField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        super(ExclusiveBooleanField, self).contribute_to_class(cls, name)
        models.signals.class_prepared.connect(self._replace_save, sender=cls)

    def _replace_save(self, sender, **kwargs):
        old_save = sender.save
        field_name = self.name
        on_fields = self._on_fields

        def new_save(self, *args, **kwargs):
            def reducer(left, right):
                return left & Q(**{right: getattr(self, right)})

            with transaction.commit_on_success():
                if getattr(self, field_name) is True:
                    f_args = reduce(reducer, on_fields, Q())
                    u_args = {field_name: False}
                    sender._default_manager.filter(f_args).update(**u_args)
                old_save(self, *args, **kwargs)
        new_save.alters_data = True

        sender.save = new_save


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules(
        rules=[],
        patterns=[
            'exclusivebooleanfield\.fields\.ExclusiveBooleanField',
        ]
    )
except ImportError:
    pass
