# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import resolve
from django.db.models import Count
from django.utils.safestring import mark_safe
from lbe.models import Setting, Article, Category, Comment


def lbe_sidebar(request):
    ctx = {}

    if not resolve(request.path).namespace == 'lbe':
        return ctx

    for snippet in Setting.template_snippets.all():
        ctx[snippet.name] = mark_safe(snippet.value)
    ctx['aside_pages_list'] = (
        Article.published_standalone.only('title', 'slug').order_by('created')
    )
    ctx['aside_category_list'] = (
        Category.objects
        .filter(article__is_published=True)
        .annotate(article_count=Count('article')).filter(article_count__gt=0)
    )
    ctx['aside_comment_list'] = (
        Comment.objects
        .filter(is_approved=True, article__is_published=True)
        .extra(select={'_article_slug': 'lbe_article.slug'})
    )[:5]
    return ctx
