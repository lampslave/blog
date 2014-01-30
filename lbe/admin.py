# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from pagedown.widgets import AdminPagedownWidget
from lbe.models import Setting, Category, Article, SpamSnippet, Comment


class SettingAdmin(admin.ModelAdmin):
    pass

admin.site.register(Setting, SettingAdmin)


class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)


class ArticleAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }

admin.site.register(Article, ArticleAdmin)


class SpamSnippetAdmin(admin.ModelAdmin):
    pass

admin.site.register(SpamSnippet, SpamSnippetAdmin)


class CommentAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }

admin.site.register(Comment, CommentAdmin)
