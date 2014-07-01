# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from pagedown.widgets import AdminPagedownWidget
from lbe.models import Setting, SpamSnippet, Category, Article, Comment


admin.site.register(Setting)
admin.site.register(SpamSnippet)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }


class CommentAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
