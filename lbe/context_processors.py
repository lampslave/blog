# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import Count
from django.utils.safestring import mark_safe
from lbe.models import Article, Category, Comment, TemplateSnippet


def lbe_sidebar(request):
    ctx = {}

    for snippet in TemplateSnippet.objects.all():
        ctx[snippet.name] = mark_safe(snippet.content)

    ctx['aside_pages_list'] = (
        Article.published_standalone.all()
        .only('title', 'slug').order_by('created')
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
