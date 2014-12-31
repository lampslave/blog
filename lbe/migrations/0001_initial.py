# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('content', models.TextField(verbose_name='\u043a\u043e\u043d\u0442\u0435\u043d\u0442')),
                ('created', models.DateTimeField(verbose_name='\u0437\u0430\u043f\u0438\u0441\u044c \u0441\u043e\u0437\u0434\u0430\u043d\u0430')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='\u0437\u0430\u043f\u0438\u0441\u044c \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0430')),
                ('slug', models.CharField(unique=True, max_length=100, verbose_name='\u043f\u0441\u0435\u0432\u0434\u043e\u043d\u0438\u043c')),
                ('description', models.CharField(max_length=255, verbose_name='\u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('is_comment_allowed', models.BooleanField(default=True, verbose_name='\u043a\u043e\u043c\u043c\u0435\u043d\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435 \u0440\u0430\u0437\u0440\u0435\u0448\u0435\u043d\u043e')),
                ('is_standalone', models.BooleanField(default=False, verbose_name='\u043d\u0435\u0437\u0430\u0432\u0438\u0441\u0438\u043c\u0430\u044f \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430')),
                ('is_published', models.BooleanField(default=False, verbose_name='\u0437\u0430\u043f\u0438\u0441\u044c \u043e\u043f\u0443\u0431\u043b\u0438\u043a\u043e\u0432\u0430\u043d\u0430')),
            ],
            options={
                'ordering': ['-created'],
                'verbose_name': '\u0437\u0430\u043f\u0438\u0441\u044c',
                'verbose_name_plural': '\u0437\u0430\u043f\u0438\u0441\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='\u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('slug', models.CharField(unique=True, max_length=100, verbose_name='\u043f\u0441\u0435\u0432\u0434\u043e\u043d\u0438\u043c')),
                ('description', models.CharField(max_length=255, verbose_name='\u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
            ],
            options={
                'verbose_name': '\u0440\u0443\u0431\u0440\u0438\u043a\u0430',
                'verbose_name_plural': '\u0440\u0443\u0431\u0440\u0438\u043a\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_name', models.CharField(max_length=50, verbose_name='\u0438\u043c\u044f')),
                ('user_email', models.EmailField(max_length=75, verbose_name='email', blank=True)),
                ('user_url', models.URLField(verbose_name='\u0441\u0430\u0439\u0442', blank=True)),
                ('content', models.TextField(verbose_name='\u043a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439')),
                ('created', models.DateTimeField(verbose_name='\u043a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439 \u0441\u043e\u0437\u0434\u0430\u043d', blank=True)),
                ('is_approved', models.BooleanField(default=False, verbose_name='\u043a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439 \u043e\u0434\u043e\u0431\u0440\u0435\u043d')),
                ('article', models.ForeignKey(verbose_name='\u0441\u0432\u044f\u0437\u0430\u043d\u043d\u0430\u044f \u0437\u0430\u043f\u0438\u0441\u044c', to='lbe.Article')),
                ('parent', models.ForeignKey(verbose_name='\u0440\u043e\u0434\u0438\u0442\u0435\u043b\u044c\u0441\u043a\u0438\u0439 \u043a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439', blank=True, to='lbe.Comment', null=True)),
            ],
            options={
                'ordering': ['-created'],
                'verbose_name': '\u043a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439',
                'verbose_name_plural': '\u043a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='\u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('value', models.CharField(max_length=255, verbose_name='\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435', blank=True)),
                ('description', models.CharField(max_length=255, verbose_name='\u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('autoload', models.BooleanField(default=True, verbose_name='\u0430\u0432\u0442\u043e\u0437\u0430\u0433\u0440\u0443\u0437\u043a\u0430 \u0432 \u0448\u0430\u0431\u043b\u043e\u043d')),
            ],
            options={
                'verbose_name': '\u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0430',
                'verbose_name_plural': '\u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SpamSnippet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('snippet', models.CharField(unique=True, max_length=255, verbose_name='\u0444\u0440\u0430\u0433\u043c\u0435\u043d\u0442')),
            ],
            options={
                'verbose_name': '\u0444\u0440\u0430\u0433\u043c\u0435\u043d\u0442',
                'verbose_name_plural': '\u0447\u0451\u0440\u043d\u044b\u0439 \u0441\u043f\u0438\u0441\u043e\u043a',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(verbose_name='\u0440\u0443\u0431\u0440\u0438\u043a\u0430', blank=True, to='lbe.Category', null=True),
            preserve_default=True,
        ),
    ]
