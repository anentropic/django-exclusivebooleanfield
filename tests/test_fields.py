import pytest

from testapp.models import UnlimitedModel, LimitedModel, RelatedModel


@pytest.mark.django_db
def test_unlimited():
    models = [UnlimitedModel.objects.create() for i in range(3)]
    assert UnlimitedModel.objects.count() == 3
    assert UnlimitedModel.objects.filter(the_one=True).count() == 0

    models[0].the_one = True
    models[0].save()
    assert UnlimitedModel.objects.filter(the_one=True).count() == 1
    assert UnlimitedModel.objects.get(the_one=True).pk == models[0].pk

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
