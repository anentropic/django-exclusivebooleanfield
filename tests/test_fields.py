import pytest

from testapp.models import (
    UnlimitedModel, LimitedModel, RelatedModel, ShorthandModel
)


@pytest.mark.django_db
def test_unlimited():
    models = [UnlimitedModel.objects.create() for i in range(3)]
    assert UnlimitedModel.objects.count() == 3
    assert UnlimitedModel.objects.filter(the_one=True).count() == 0

    models[0].the_one = True
    models[0].save()
    assert UnlimitedModel.objects.filter(the_one=True).count() == 1
    assert UnlimitedModel.objects.get(the_one=True).pk == models[0].pk
    assert models[0].overridden_save is True

    models[1].the_one = True
    models[1].save()
    assert UnlimitedModel.objects.filter(the_one=True).count() == 1
    assert UnlimitedModel.objects.get(the_one=True).pk == models[1].pk

    models[2].the_one = True
    models[2].save()
    assert UnlimitedModel.objects.filter(the_one=True).count() == 1
    assert UnlimitedModel.objects.get(the_one=True).pk == models[2].pk


@pytest.mark.django_db
def test_limited():
    relations = [RelatedModel.objects.create() for i in range(2)]

    LimitedModel.objects.create(related=relations[0], value=1, the_one=True)
    LimitedModel.objects.create(related=relations[0], value=2, the_one=True)
    models = [
        LimitedModel.objects.create(related=relations[1], value=1)
        for i in range(3)
    ]
    filter_kwargs = {
        'the_one': True,
        'related__pk': relations[1].pk,
    }
    assert LimitedModel.objects.count() == 5
    assert LimitedModel.objects.filter(**filter_kwargs).count() == 0

    models[0].the_one = True
    models[0].save()
    assert LimitedModel.objects.filter(**filter_kwargs).count() == 1
    assert LimitedModel.objects.get(**filter_kwargs).pk == models[0].pk

    models[1].the_one = True
    models[1].save()
    assert LimitedModel.objects.filter(**filter_kwargs).count() == 1
    assert LimitedModel.objects.get(**filter_kwargs).pk == models[1].pk

    models[2].the_one = True
    models[2].save()
    assert LimitedModel.objects.filter(**filter_kwargs).count() == 1
    assert LimitedModel.objects.get(**filter_kwargs).pk == models[2].pk


@pytest.mark.django_db
def test_shorthand():
    ShorthandModel.objects.create(value=2, the_one=True)
    models = [
        ShorthandModel.objects.create(value=1)
        for i in range(3)
    ]
    filter_kwargs = {
        'the_one': True,
        'value': 1,
    }
    assert ShorthandModel.objects.count() == 4
    assert ShorthandModel.objects.filter(**filter_kwargs).count() == 0
    assert ShorthandModel.objects.filter(value=2, the_one=True).count() == 1

    models[0].the_one = True
    models[0].save()
    assert ShorthandModel.objects.filter(**filter_kwargs).count() == 1
    assert ShorthandModel.objects.get(**filter_kwargs).pk == models[0].pk
    assert ShorthandModel.objects.filter(value=2, the_one=True).count() == 1

    models[1].the_one = True
    models[1].save()
    assert ShorthandModel.objects.filter(**filter_kwargs).count() == 1
    assert ShorthandModel.objects.get(**filter_kwargs).pk == models[1].pk
    assert ShorthandModel.objects.filter(value=2, the_one=True).count() == 1

    models[2].the_one = True
    models[2].save()
    assert ShorthandModel.objects.filter(**filter_kwargs).count() == 1
    assert ShorthandModel.objects.get(**filter_kwargs).pk == models[2].pk
    assert ShorthandModel.objects.filter(value=2, the_one=True).count() == 1


def test_atomic():
    import django
    from django.db import transaction
    from exclusivebooleanfield.fields import transaction_context
    # eg django.VERSION == (1, 4, 9, 'final', 0)
    if django.VERSION[1] >= 6:
        assert transaction_context == transaction.atomic
    else:
        assert transaction_context == transaction.commit_on_success
