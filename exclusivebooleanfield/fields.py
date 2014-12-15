from django.db import models, transaction
from django.db.models import Q
from django.utils.six import string_types


try:
    transaction_context = transaction.atomic
except AttributeError:
    transaction_context = transaction.commit_on_success


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
        if isinstance(on, string_types):
            on = (on, )
        self._on_fields = on or ()
        super(ExclusiveBooleanField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        super(ExclusiveBooleanField, self).contribute_to_class(cls, name)
        models.signals.class_prepared.connect(self._replace_save, sender=cls)

    def deconstruct(self):
        """
        to support Django 1.7 migrations, see also the add_introspection_rules
        section at bottom of this file for South + earlier Django versions
        """
        name, path, args, kwargs = super(ExclusiveBooleanField, self).deconstruct()
        if self._on_fields:
            kwargs['on'] = self._on_fields
        return name, path, args, kwargs

    def _replace_save(self, sender, **kwargs):
        old_save = sender.save
        field_name = self.name
        on_fields = self._on_fields

        def new_save(self, *args, **kwargs):
            def reducer(left, right):
                return left & Q(**{right: getattr(self, right)})

            with transaction_context():
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
        rules=[
            (
                (ExclusiveBooleanField,),
                [],
                {"on": ["_on_fields", {"default": tuple()}]},
            )
        ],
        patterns=[
            'exclusivebooleanfield\.fields\.ExclusiveBooleanField',
        ]
    )
except ImportError:
    pass
