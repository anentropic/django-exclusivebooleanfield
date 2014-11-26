from south.orm import FakeORM
from south.v2 import DataMigration


def apply_south_migration(migration_cls, *_args, **_kwargs):
    orm = FakeORM(migration_cls, 'testapp')
    migration_instance = migration_cls()
    migration_instance.forwards(orm)


FROZEN_MODELS = {
    'testapp.limitedmodel': {
        'Meta': {'object_name': 'LimitedModel'},
        'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
        'related': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testapp.RelatedModel']", 'null': 'True'}),
        'the_one': ('exclusivebooleanfield.fields.ExclusiveBooleanField', [], {'default': 'False', 'on': "('related', 'value')"}),
        'value': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
    },
    'testapp.relatedmodel': {
        'Meta': {'object_name': 'RelatedModel'},
        'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
    },
    'testapp.shorthandmodel': {
        'Meta': {'object_name': 'ShorthandModel'},
        'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
        'the_one': ('exclusivebooleanfield.fields.ExclusiveBooleanField', [], {'default': 'False', 'on': "('value',)"}),
        'value': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
    },
    'testapp.unlimitedmodel': {
        'Meta': {'object_name': 'UnlimitedModel'},
        'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
        'the_one': ('exclusivebooleanfield.fields.ExclusiveBooleanField', [], {'default': 'False'})
    }
}


class BaseDataMigration(DataMigration):
    models = FROZEN_MODELS

    complete_apps = ['testapp']
    symmetrical = True


class UnlimitedMigration(BaseDataMigration):
    def forwards(self, orm):
        for i in range(3):
            orm.UnlimitedModel.objects.create(the_one=True)


class ShorthandMigration(BaseDataMigration):
    def forwards(self, orm):
        orm.ShorthandModel.objects.create(the_one=True, value=2)
        for i in range(3):
            orm.ShorthandModel.objects.create(the_one=True, value=1)


class LimitedMigration1(BaseDataMigration):
    def forwards(self, orm):
        relations = [orm.RelatedModel.objects.create(id=i) for i in range(2)]
        orm.LimitedModel.objects.create(related=relations[0], value=1, the_one=True)
        orm.LimitedModel.objects.create(related=relations[0], value=2, the_one=True)
        for i in range(3):
            orm.LimitedModel.objects.create(related=relations[1], value=1)


class LimitedMigration2(BaseDataMigration):
    def forwards(self, orm):
        instance = orm.LimitedModel.objects.filter(related__pk=1, value=1)[0]
        instance.the_one = True
        instance.save()
