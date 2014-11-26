import pytest

from testapp.models import (
    UnlimitedModel, LimitedModel, RelatedModel, ShorthandModel
)

try:
    import south
except ImportError:
    from migrations.django_migrations import (
        apply_django_migration, LimitedMigration1, LimitedMigration2,
        ShorthandMigration, UnlimitedMigration
    )
    apply_migration = apply_django_migration
else:
    from migrations.south_migrations import (
        apply_south_migration, LimitedMigration1, LimitedMigration2,
        ShorthandMigration, UnlimitedMigration
    )
    apply_migration = apply_south_migration


@pytest.mark.django_db
def test_unlimited():
    assert UnlimitedModel.objects.count() == 0

    apply_migration(UnlimitedMigration)

    assert UnlimitedModel.objects.count() == 3
    assert UnlimitedModel.objects.filter(the_one=True).count() == 1


@pytest.mark.django_db
def test_shorthand():
    assert ShorthandModel.objects.count() == 0

    apply_migration(ShorthandMigration)

    assert ShorthandModel.objects.count() == 4
    assert ShorthandModel.objects.filter(the_one=True, value=1).count() == 1
    assert ShorthandModel.objects.filter(the_one=True, value=2).count() == 1


@pytest.mark.django_db
def test_limited():
    assert RelatedModel.objects.count() == 0
    assert LimitedModel.objects.count() == 0

    executor = apply_migration(LimitedMigration1, '0002')

    filter_kwargs = {
        'the_one': True,
        'related__pk': 1,
    }
    assert LimitedModel.objects.count() == 5
    assert LimitedModel.objects.filter(**filter_kwargs).count() == 0

    apply_migration(LimitedMigration2, '0003', executor=executor)

    assert LimitedModel.objects.filter(**filter_kwargs).count() == 1
