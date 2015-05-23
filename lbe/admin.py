# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib import admin
from pagedown.widgets import AdminPagedownWidget
from lbe.models import Setting, SpamSnippet, Category, Article, Comment, \
    TemplateSnippet
from lbe.widgets import AdminCodeMirrorWidget


admin.site.register(TemplateSnippet)
admin.site.register(Setting)
admin.site.register(SpamSnippet)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('is_published', 'is_standalone', 'is_comment_allowed',)
    prepopulated_fields = {'slug': ('title', )}
    formfield_overrides = {
        models.TextField: {'widget': AdminCodeMirrorWidget},
    }


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'content', 'is_approved',)
    list_filter = ('is_approved',)
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
