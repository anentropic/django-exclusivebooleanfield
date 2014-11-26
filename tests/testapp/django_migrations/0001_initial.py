# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import exclusivebooleanfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LimitedModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField(null=True)),
                ('the_one', exclusivebooleanfield.fields.ExclusiveBooleanField(default=False, on=(b'related', b'value'))),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RelatedModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShorthandModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField(null=True)),
                ('the_one', exclusivebooleanfield.fields.ExclusiveBooleanField(default=False, on=(b'value',))),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UnlimitedModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('the_one', exclusivebooleanfield.fields.ExclusiveBooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='limitedmodel',
            name='related',
            field=models.ForeignKey(to='testapp.RelatedModel', null=True),
            preserve_default=True,
        ),
    ]
