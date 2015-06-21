# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import Count
from django.utils.safestring import mark_safe
from lbe.models import Article, Category, Comment, TemplateSnippet


def lbe_sidebar(request):
    ctx = {}

    for snippet in TemplateSnippet.objects.all():
        ctx[snippet.name] = mark_safe(snippet.content)

    pages = Article.objects.published_standalone()
    ctx['aside_pages_list'] = pages.only('title', 'slug').order_by('created')

    categories = Category.objects.filter(article__is_published=True)
    ctx['aside_category_list'] = \
        categories.annotate(Count('article')).filter(article__count__gt=0)

    commensts = Comment.objects.filter(is_approved=True,
                                       article__is_published=True)
    ctx['aside_comment_list'] = \
        commensts.extra(select={'_article_slug': 'lbe_article.slug'})[:5]

    return ctx
