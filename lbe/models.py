# -*- coding: utf-8 -*-
import re
import hashlib
from markdown2 import markdown
from django.db import models
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.utils import timezone


class Setting(models.Model):
    name = models.CharField(unique=True, max_length=255, verbose_name=_('setting name'))
    value = models.CharField(blank=True, max_length=255, verbose_name=_('setting value'))
    description = models.CharField(blank=True, max_length=255, verbose_name=_('setting description'))
    autoload = models.BooleanField(default=True, verbose_name=_('autoload as template variable'))

    class Meta():
        verbose_name = _('setting')
        verbose_name_plural = _('settings')

    def __unicode__(self):
        return u'{}: {}'.format(self.name, self.description[:50])

    def clean(self):
        self.name = self.name.strip().replace('-', '_')
        e = re.compile('[^a-z_]')
        if e.search(self.name) is not None:
            raise ValidationError(_('Invalid name (a-z and _ only)'))


class Category(models.Model):
    name = models.CharField(unique=True, max_length=255, verbose_name=_('category name'))
    slug = models.CharField(unique=True, max_length=100, verbose_name=_('category slug'))
    description = models.CharField(blank=True, max_length=255, verbose_name=_('category description'))

    class Meta():
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return  reverse('lbe:category', args=[self.slug])


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('article title'))
    content = models.TextField(verbose_name=_('article content'))
    created = models.DateTimeField(verbose_name=_('article created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('article updated'))
    category = models.ForeignKey(Category, blank=True, null=True, verbose_name=_('related category'))
    slug = models.CharField(unique=True, max_length=100, verbose_name=_('article slug'))
    description = models.CharField(blank=True, max_length=255, verbose_name=_('article description'))
    is_comment_allowed = models.BooleanField(default=True, verbose_name=_('comment allowed'))
    is_standalone = models.BooleanField(default=False, verbose_name=_('standalone page'))
    is_published = models.BooleanField(default=False, verbose_name=_('article published'))

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
        return reverse('lbe:article', args=[self.slug])


class SpamSnippet(models.Model):
    snippet = models.CharField(unique=True, max_length=255, verbose_name=_('snippet'))

    class Meta():
        verbose_name = _('spam snippet')
        verbose_name_plural = _('spam snippets')

    def __unicode__(self):
        return self.snippet[:30]


class Comment(models.Model):
    article = models.ForeignKey(Article, verbose_name=_('related article'))
    parent = models.ForeignKey('self', blank=True, null=True, verbose_name=_('parent comment'))
    user_name = models.CharField(max_length=50, verbose_name=_('name'))
    user_email = models.EmailField(blank=True, verbose_name='email')  # FIXME translation is off
    user_url = models.URLField(blank=True, verbose_name=_('website'))
    content = models.TextField(verbose_name=_('comment'))
    created = models.DateTimeField(blank=True, null=False, verbose_name=_('comment created'))
    is_approved = models.BooleanField(default=False, verbose_name=_('comment approved'))

    class Meta():
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    def __unicode__(self):
        content = strip_tags(self.get_content())
        return u'{}: {}...'.format(self.user_name, content[:40].rstrip())

    def get_content(self):
        return mark_safe(markdown(self.content, html4tags=True,
                                  safe_mode='escape'))

    def get_user_avatar(self):
        return ''.join(["http://www.gravatar.com/avatar/",
                        hashlib.md5(self.user_email).hexdigest()])

    def get_reply_link(self):
        return reverse('lbe:comment_reply', args=[self.article_id, self.pk])

    def get_absolute_url(self):
        article_url = (Article.objects.only('slug').get(pk=self.article_id)
                       .get_absolute_url())
        return u'{}#comment-{}'.format(article_url, self.pk)

    def clean(self):
        if not self.created:
            self.created = timezone.now()
        if not (Article.objects.only('is_comment_allowed')
                .get(pk=self.article_id).is_comment_allowed):
            raise PermissionDenied()
        if self.user_name.startswith('http://'):
            raise PermissionDenied()
        # spambots usually put both <a> and [url] tags into comment
        if '<a' in self.content and '[url' in self.content:
            raise PermissionDenied()
        # blacklist
        spam = SpamSnippet.objects.values_list('snippet')
        for (s, ) in spam:
            if any(s in data for data in (self.user_name, self.user_email,
                                          self.user_url, self.content)):
                raise PermissionDenied()
