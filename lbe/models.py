# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import hashlib
from urlparse import urlparse
from markdown2 import markdown
from django.db import models
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.utils import timezone


class TemplateSnippet(models.Model):
    name = models.CharField(_('snippet name'), unique=True, max_length=255)
    content = models.TextField(_('snippet content'))
    description = models.CharField(
        _('snippet description'), blank=True, max_length=255
    )

    class Meta():
        verbose_name = _('template snippet')
        verbose_name_plural = _('template snippets')

    def __unicode__(self):
        return '{}: {}'.format(self.name, self.description[:50])

    def clean(self):
        if re.compile('[^a-z_]').search(self.name) is not None:
            raise ValidationError(_('Invalid name (a-z and _ only)'))


class Setting(models.Model):
    name = models.CharField(_('setting name'), unique=True, max_length=255)
    value = models.CharField(_('setting value'), blank=True, max_length=255)
    description = models.CharField(
        _('setting description'), blank=True, max_length=255
    )

    class Meta():
        verbose_name = _('setting')
        verbose_name_plural = _('settings')

    def __unicode__(self):
        return '{}: {}'.format(self.name, self.description[:50])

    def clean(self):
        if re.compile('[^a-z_]').search(self.name) is not None:
            raise ValidationError(_('Invalid name (a-z and _ only)'))


class Category(models.Model):
    name = models.CharField(_('category name'), unique=True, max_length=255)
    slug = models.CharField(_('category slug'), unique=True, max_length=100)
    description = models.CharField(
        _('category description'), blank=True, max_length=255
    )

    class Meta():
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('lbe:category', args=[self.slug])


class RegularArticleManager(models.Manager):
    def get_queryset(self):
        qs = super(RegularArticleManager, self).get_queryset()
        return qs.filter(is_standalone=False, is_published=True)


class StandaloneArticleManager(models.Manager):
    def get_queryset(self):
        qs = super(StandaloneArticleManager, self).get_queryset()
        return qs.filter(is_standalone=True, is_published=True)


class Article(models.Model):
    title = models.CharField(_('article title'), max_length=255)
    content = models.TextField(_('article content'))
    created = models.DateTimeField(_('article created'))
    updated = models.DateTimeField(_('article updated'), auto_now=True)
    category = models.ForeignKey(
        Category, verbose_name=_('related category'), blank=True, null=True
    )
    slug = models.CharField(_('article slug'), unique=True, max_length=100)
    description = models.CharField(
        _('article description'), blank=True, max_length=255
    )
    is_comment_allowed = models.BooleanField(_('comment allowed'), default=True)
    is_standalone = models.BooleanField(_('standalone page'), default=False)
    is_published = models.BooleanField(_('article published'), default=False)

    objects = models.Manager()
    published_regular = RegularArticleManager()
    published_standalone = StandaloneArticleManager()

    class Meta():
        ordering = ['-created']
        verbose_name = _('article')
        verbose_name_plural = _('articles')

    def __unicode__(self):
        return self.title

    def get_content(self):
        return mark_safe(markdown(self.content, html4tags=True,
                                  safe_mode=None))

    def get_description(self):
        return self.description or (strip_tags(self.get_content())[:160]
                                    .replace('\n', ' ').replace('\r', ' '))

    def get_absolute_url(self):
        # this expression also used in Comment.get_absolute_url()
        return reverse('lbe:article', args=[self.slug])


class SpamSnippet(models.Model):
    snippet = models.CharField(_('snippet'), unique=True, max_length=255)

    class Meta():
        verbose_name = _('spam snippet')
        verbose_name_plural = _('spam snippets')

    def __unicode__(self):
        return self.snippet[:30]


class Comment(models.Model):
    article = models.ForeignKey(Article, verbose_name=_('related article'))
    parent = models.ForeignKey(
        'self', verbose_name=_('parent comment'), blank=True, null=True
    )
    user_name = models.CharField(_('name'), max_length=50)
    user_email = models.EmailField(_('email'), blank=True)
    user_url = models.URLField(_('website'), blank=True)
    content = models.TextField(_('comment'))
    created = models.DateTimeField(_('comment created'), blank=True, null=False)
    is_approved = models.BooleanField(_('comment approved'), default=False)

    class Meta():
        ordering = ['-created']
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    def __unicode__(self):
        content = strip_tags(self.get_content())
        return '{}: {}...'.format(self.user_name, content[:40].rstrip())

    def get_content(self):
        return mark_safe(markdown(self.content, html4tags=True,
                                  safe_mode='escape'))

    def get_user_avatar(self):
        return ''.join(["http://www.gravatar.com/avatar/",
                        hashlib.md5(self.user_email).hexdigest()])

    def get_reply_link(self):
        return reverse('lbe:comment_reply', args=[self.article_id, self.id])

    _article_slug = None
    _article_url = None

    def get_absolute_url(self):
        # article slug can be fetched in same query with .extra()
        if self._article_slug is not None:
            self._article_url = reverse(
                'lbe:article', args=[self._article_slug]
            )
        if self._article_url is None:
            self._article_url = (
                Article.objects.only('slug').get(id=self.article_id)
                .get_absolute_url()
            )
        return '{}#comment-{}'.format(self._article_url, self.id)

    def clean(self):
        if not self.created:
            self.created = timezone.now()

        article = (
            Article.objects.only('is_comment_allowed')
            .filter(pk=self.article_id).first()
        )
        if not getattr(article, 'is_comment_allowed', False):
            raise PermissionDenied()

        spam = SpamSnippet.objects.values_list('snippet')
        fields = (self.user_name, self.user_email, self.user_url, self.content)
        for (snippet, ) in spam:
            if any(snippet.lower() in field.lower() for field in fields):
                raise PermissionDenied()

        if (self.user_name.startswith('http://') or
                self.user_name.endswith(('.com', '.org', '.net'))):
            raise ValidationError({
                'user_name': [_('Links are not allowed here'), ]
            })

        url = urlparse(self.user_url)
        if len(url.path) > 10 or len(url.query) > 10:
            raise ValidationError({
                'user_url': [_('This link is too long'), ]
            })

        if any(markup in self.content for markup in ('<a href', '[url')) or \
                self.content.startswith('http://'):
            raise ValidationError({
                'content': [_('Please, use Markdown syntax for links'), ]
            })
