# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UnlimitedModel'
        db.create_table('testapp_unlimitedmodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('the_one', self.gf('exclusivebooleanfield.fields.ExclusiveBooleanField')(default=False)),
        ))
        db.send_create_signal('testapp', ['UnlimitedModel'])

        # Adding model 'RelatedModel'
        db.create_table('testapp_relatedmodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('testapp', ['RelatedModel'])

        # Adding model 'LimitedModel'
        db.create_table('testapp_limitedmodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('related', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['testapp.RelatedModel'], null=True)),
            ('value', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('the_one', self.gf('exclusivebooleanfield.fields.ExclusiveBooleanField')(default=False, on=('related', 'value'))),
        ))
        db.send_create_signal('testapp', ['LimitedModel'])

        # Adding model 'ShorthandModel'
        db.create_table('testapp_shorthandmodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('the_one', self.gf('exclusivebooleanfield.fields.ExclusiveBooleanField')(default=False, on=('value',))),
        ))
        db.send_create_signal('testapp', ['ShorthandModel'])


    def backwards(self, orm):
        # Deleting model 'UnlimitedModel'
        db.delete_table('testapp_unlimitedmodel')

        # Deleting model 'RelatedModel'
        db.delete_table('testapp_relatedmodel')

        # Deleting model 'LimitedModel'
        db.delete_table('testapp_limitedmodel')

        # Deleting model 'ShorthandModel'
        db.delete_table('testapp_shorthandmodel')


    models = {
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

    complete_apps = ['testapp']