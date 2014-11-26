from django.db import connections, DEFAULT_DB_ALIAS, migrations
from django.db.migrations.executor import MigrationExecutor


def apply_django_migration(migration_cls, migration_name='9999',
                           app_label='testapp', executor=None):
    if executor is None:
        executor = MigrationExecutor(connections[DEFAULT_DB_ALIAS])
    migration = migration_cls(migration_name, app_label)
    key = (migration.app_label, migration.name)

    executor.loader.graph.add_node(key, migration)
    for parent in migration.dependencies:
        executor.loader.graph.add_dependency(migration, key, parent)

    executor.apply_migration(migration)
    return executor


def migration_create_factory(app_name, model_name, create_kwargs=None):
    create_kwargs = create_kwargs or {}

    def migration_operation(apps, schema_editor):
        Model = apps.get_model(app_name, model_name)
        instance = Model(**create_kwargs)
        instance.save()

    return migration_operation


def migration_update_factory(app_name, model_name, update_kwargs,
                             filter_kwargs=None):
    filter_kwargs = filter_kwargs or {}

    def migration_operation(apps, schema_editor):
        Model = apps.get_model(app_name, model_name)
        Model._default_manager.filter(**filter_kwargs).update(**update_kwargs)

    return migration_operation


class UnlimitedMigration(migrations.Migration):
    dependencies = [
        ('testapp', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            migration_create_factory('testapp', 'UnlimitedModel',
                                     {'the_one': True})
        ),
        migrations.RunPython(
            migration_create_factory('testapp', 'UnlimitedModel',
                                     {'the_one': True})
        ),
        migrations.RunPython(
            migration_create_factory('testapp', 'UnlimitedModel',
                                     {'the_one': True})
        ),
    ]


class ShorthandMigration(migrations.Migration):
    dependencies = [
        ('testapp', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            migration_create_factory('testapp', 'ShorthandModel',
                                     {'the_one': True, 'value': 2})
        ),
    ] + ([
        migrations.RunPython(
            migration_create_factory('testapp', 'ShorthandModel',
                                     {'the_one': True, 'value': 1})
        ),
    ] * 3)


class LimitedMigration1(migrations.Migration):
    dependencies = [
        ('testapp', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            migration_create_factory('testapp', 'RelatedModel', {'id': 0})
        ),
        migrations.RunPython(
            migration_create_factory('testapp', 'RelatedModel', {'id': 1})
        ),
        migrations.RunPython(
            migration_create_factory(
                'testapp',
                'LimitedModel',
                {'related_id': 0, 'the_one': True, 'value': 1}
            )
        ),
        migrations.RunPython(
            migration_create_factory(
                'testapp',
                'LimitedModel',
                {'related_id': 0, 'the_one': True, 'value': 2}
            )
        ),
    ] + ([
        migrations.RunPython(
            migration_create_factory(
                'testapp',
                'LimitedModel',
                {'related_id': 1, 'value': 1}
            )
        ),
    ] * 3)


def update_model(apps, schema_editor):
    ModelCls = apps.get_model('testapp', 'LimitedModel')
    instance = ModelCls.objects.filter(related__pk=1, value=1)[0]
    instance.the_one = True
    instance.save()


class LimitedMigration2(migrations.Migration):
    dependencies = [
        ('testapp', '0001_initial'),
        ('testapp', '0002'),
    ]

    operations = [
        migrations.RunPython(update_model),
    ]
