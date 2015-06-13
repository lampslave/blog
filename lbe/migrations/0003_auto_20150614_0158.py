# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lbe', '0002_add_template_snippet_model_and_migrate_settings'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='templatesnippet',
            options={'verbose_name': '\u0441\u043d\u0438\u043f\u043f\u0435\u0442', 'verbose_name_plural': '\u0441\u043d\u0438\u043f\u043f\u0435\u0442\u044b'},
        ),
        migrations.AlterField(
            model_name='comment',
            name='user_email',
            field=models.EmailField(max_length=254, verbose_name='email', blank=True),
        ),
        migrations.AlterField(
            model_name='templatesnippet',
            name='content',
            field=models.TextField(verbose_name='\u043a\u043e\u043d\u0442\u0435\u043d\u0442'),
        ),
        migrations.AlterField(
            model_name='templatesnippet',
            name='description',
            field=models.CharField(max_length=255, verbose_name='\u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True),
        ),
        migrations.AlterField(
            model_name='templatesnippet',
            name='name',
            field=models.CharField(unique=True, max_length=255, verbose_name='\u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
    ]
