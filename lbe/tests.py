# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone as tz
from django.utils.html import escape
from django.utils.encoding import force_text
from lbe.models import Article, Category, Comment
from lbe.utils import random_string as rs, random_text as rt, \
    random_char_seq as rcs


class Test(TestCase):
    def test_article_detail(self):
        article = Article.objects.create(
            title=rs(20), content=rt(4), created=tz.now(), slug=rcs(10)
        )

        response = self.client.get(article.get_absolute_url())
        self.assertEqual(response.status_code, 404)

        article.is_published = True
        article.save()
        response = self.client.get(article.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(article, response.context['object'])
        self.assertIn(str(article.title), response.content)
        self.assertIn(str(article.get_content()), response.content)

    def test_article_list_and_feed(self):
        response = self.client.get(reverse('lbe:article_list'))
        self.assertEqual(response.status_code, 200)

        article_pub = Article.objects.create(
            title=rs(20), content=rt(4), created=tz.now(), slug=rcs(10),
            is_published=True
        )
        article_not_pub = Article.objects.create(
            title=rs(20), content=rt(4), created=tz.now(), slug=rcs(10)
        )
        page_pub = Article.objects.create(
            title=rs(20), content=rt(4), created=tz.now(), slug=rcs(10),
            is_standalone=True, is_published=True
        )
        page_not_pub = Article.objects.create(
            title=rs(20), content=rt(4), created=tz.now(), slug=rcs(10),
            is_standalone=True
        )

        response = self.client.get(reverse('lbe:article_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(article_pub, response.context['object_list'])
        for a in (article_not_pub, page_pub, page_not_pub):
            self.assertNotIn(a, response.context['object_list'])

        response = self.client.get(reverse('lbe:rss'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(escape(article_pub.get_content()), force_text(response))
        for a in (article_not_pub, page_pub, page_not_pub):
            self.assertNotIn(escape(a.get_content()), force_text(response))

    def test_category_list_and_feed(self):
        response = self.client.get(
            reverse('lbe:category', args=[rcs(10)])
        )
        self.assertEqual(response.status_code, 404)

        article_pub = Article.objects.create(
            title=rs(20), content=rt(4), created=tz.now(), slug=rcs(10),
            is_published=True
        )
        article_not_pub = Article.objects.create(
            title=rs(20), content=rt(4), created=tz.now(), slug=rcs(10)
        )
        page_pub = Article.objects.create(
            title=rs(20), content=rt(4), created=tz.now(), slug=rcs(10),
            is_standalone=True, is_published=True
        )
        page_not_pub = Article.objects.create(
            title=rs(20), content=rt(4), created=tz.now(), slug=rcs(10),
            is_standalone=True
        )

        response = self.client.get(
            reverse('lbe:category', args=[rcs(10)])
        )
        self.assertEqual(response.status_code, 404)

        category = Category.objects.create(name=rs(20), slug=rcs(10))

        response = self.client.get(
            reverse('lbe:category', args=[category.slug])
        )
        self.assertEqual(response.status_code, 200)
        for a in (article_pub, article_not_pub, page_pub, page_not_pub):
            self.assertNotIn(a, response.context['object_list'])

        Article.objects.all().update(category=category)

        response = self.client.get(
            reverse('lbe:category', args=[category.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(article_pub, response.context['object_list'])
        for a in (article_not_pub, page_pub, page_not_pub):
            self.assertNotIn(a, response.context['object_list'])

        response = self.client.get(
            reverse('lbe:category_rss', args=[category.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(escape(article_pub.get_content()), force_text(response))
        for a in (article_not_pub, page_pub, page_not_pub):
            self.assertNotIn(escape(a.get_content()), force_text(response))

    def test_comment_add(self):
        data = {
            'user_name': rs(10),
            'content': rt(1)
        }

        response = self.client.post(reverse('lbe:comment_add'), data=data)
        self.assertEqual(response.status_code, 403)

        article = Article.objects.create(
            title=rs(20), content=rt(4), created=tz.now(), slug=rcs(10),
            is_published=True, is_comment_allowed=False
        )
        data['article'] = article.id

        response = self.client.post(reverse('lbe:comment_add'), data=data)
        self.assertEqual(response.status_code, 403)

        article.is_comment_allowed = True
        article.save()

        response = self.client.post(reverse('lbe:comment_add'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Comment.objects.filter(user_name=data['user_name']).exists(), True
        )

    def test_article_comments_rss(self):
        article = Article.objects.create(
            title=rs(20), content=rt(4), created=tz.now(), slug=rcs(10),
            is_published=True
        )

        response = self.client.get(
            reverse('lbe:article_comments_rss', args=[article.slug])
        )
        self.assertEqual(response.status_code, 200)

        comment_approved = Comment.objects.create(
            article=article, user_name=rs(10), content=rt(1), created=tz.now(),
            is_approved=True
        )
        comment_not_approved = Comment.objects.create(
            article=article, user_name=rs(10), content=rt(1), created=tz.now(),
            is_approved=False
        )

        response = self.client.get(
            reverse('lbe:article_comments_rss', args=[article.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            escape(comment_approved.get_content()), force_text(response)
        )
        self.assertNotIn(
            escape(comment_not_approved.get_content()), force_text(response)
        )
