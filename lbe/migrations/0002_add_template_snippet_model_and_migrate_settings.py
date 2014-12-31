# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def migrate_data(apps, schema_editor):
    Setting = apps.get_model('lbe', 'Setting')
    TemplateSnippet = apps.get_model('lbe', 'TemplateSnippet')
    for setting in Setting.objects.filter(autoload=True):
        TemplateSnippet.objects.create(name=setting.name, content=setting.value)
        setting.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('lbe', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemplateSnippet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='snippet name')),
                ('content', models.TextField(verbose_name='snippet content')),
                ('description', models.CharField(max_length=255, verbose_name='snippet description', blank=True)),
            ],
            options={
                'verbose_name': 'template snippet',
                'verbose_name_plural': 'template snippets',
            },
            bases=(models.Model,),
        ),
        migrations.RunPython(
            migrate_data
        ),
        migrations.RemoveField(
            model_name='setting',
            name='autoload',
        ),
    ]
