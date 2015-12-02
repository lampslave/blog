# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from lbe.views import ArticleList, ArticleDetail, CategoryList, CommentAdd, \
    CommentReply, RSS, CategoryRSS, ArticleCommentsRSS

urlpatterns = [
    url(r'^$', ArticleList.as_view(), name='article_list'),
    url(r'^feed/$', RSS(), name='rss'),
    url(r'^category/(?P<slug>[-_\w]+)/$', CategoryList.as_view(), name='category'),
    url(r'^category/(?P<slug>[-_\w]+)/feed/$', CategoryRSS(), name='category_rss'),
    url(r'^comment/add/$', CommentAdd.as_view(), name='comment_add'),
    url(r'^comment/reply/(?P<article>\d+)/(?P<pk>\d+)$', CommentReply.as_view(), name='comment_reply'),
    url(r'^(?P<slug>[-_\w]+)/$', ArticleDetail.as_view(), name='article'),
    url(r'^(?P<slug>[-_\w]+)/comments/feed/$', ArticleCommentsRSS(), name='article_comments_rss'),
]
