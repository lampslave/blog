# -*- coding: utf-8 -*-
from django.views.generic import DetailView, ListView
from django.views.generic.base import ContextMixin
from django.views.generic.edit import CreateView
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.contrib.syndication.views import Feed
from lbe.models import Setting, Category, Article, Comment
from lbe.forms import CommentForm
from lbe.utils import make_tree
from urlparse import urlparse


def add_user_session_data(instance, form_initial):
    data = instance.request.session.get('user_data', {})
    form_initial.update(data)
    return form_initial


def get_aside_content():
    data = {}
    settings = (Setting.objects.filter(autoload=True)
                .values_list('name', 'value'))
    for name, value in settings:
        data[name] = mark_safe(value)

    data['aside_pages_list'] = (Article
        .objects.filter(is_published=True, is_standalone=True)
        .order_by('created').only('title', 'slug'))

    data['aside_category_list'] = (Category.objects.annotate(Count('article'))
                                   .filter(article__count__gt=0))

    comments = (Comment.objects.filter(is_approved=True,
                                       article__is_published=True)
                .order_by('-created')[:5])
    for c in comments:
        c.get_absolute_url = c.get_absolute_url()  # caching
    data['aside_comment_list'] = comments
    return data


class AsideMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        data = super(AsideMixin, self).get_context_data(**kwargs)
        data.update(get_aside_content())
        return data


class ArticleDetail(DetailView, AsideMixin):
    model = Article

    def get_queryset(self):
        return (super(ArticleDetail, self)
                .get_queryset().filter(is_published=True))

    def get_context_data(self, **kwargs):
        data = super(ArticleDetail, self).get_context_data(**kwargs)
        comments = (Comment.objects
                    .filter(article_id=self.get_object().id).order_by('id'))
        for c in comments:
            if not c.is_approved:
                c.url = ''
                c.content = _('Comment is under moderation')
                c.under_moderation_class = 'comment-under-moderation'
        data['comment_tree'] = make_tree(comments)
        data['comment_form'] = CommentForm(
            initial=add_user_session_data(self, {'article': self.object}))
        return data


class ArticleList(ListView, AsideMixin):
    model = Article
    paginate_by = 10

    def get_queryset(self):
        return (super(ArticleList, self)
                .get_queryset().filter(is_published=True, is_standalone=False)
                .annotate(Count('comment')))


class CategoryList(ArticleList, AsideMixin):
    def get_category(self):
        return get_object_or_404(Category, slug=self.kwargs['slug'])

    def get_queryset(self):
        return (super(CategoryList, self).get_queryset()
                .filter(category=self.get_category()))

    def get_context_data(self, **kwargs):
        data = super(CategoryList, self).get_context_data(**kwargs)
        data['category'] = self.get_category()
        return data


class CommentAdd(CreateView, AsideMixin):
    model = Comment
    form_class = CommentForm
    http_method_names = ['post']
    template_name = 'lbe/comment_add.html'

    def form_valid(self, form):
        if 'user_data' not in self.request.session:
            self.request.session['user_data'] = {}
        for i in form.cleaned_data:
            if i.startswith('user_'):
                self.request.session['user_data'][i] = form.cleaned_data[i]
        if self.request.user.is_superuser:
            form.instance.is_approved = True
        return super(CommentAdd, self).form_valid(form)


class CommentReply(CommentAdd):
    http_method_names = ['get', 'post']

    def get_initial(self):
        # GET method is allowed, so we need to have some antispam protection
        article = Article.objects.only('slug').get(id=self.kwargs['article'])
        referer = urlparse(self.request.META.get('HTTP_REFERER', ''))
        if article.slug not in referer.path:  # /slug/
            raise PermissionDenied()
        return add_user_session_data(self, {'article': self.kwargs['article'],
                                            'parent': self.kwargs['pk']})


class RSS(Feed):
    def title(self):
        try:
            return Setting.objects.get(name='site_title').value
        except ObjectDoesNotExist:
            return ''

    def description(self):
        try:
            return Setting.objects.get(name='site_description').value
        except ObjectDoesNotExist:
            return ''

    def link(self):
        return reverse('lbe:rss')

    def items(self):
        return (Article.objects.filter(is_published=True,
                                       is_standalone=False)[:10])

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.get_content()

    def item_pubdate(self, item):
        return item.created


class CategoryRSS(RSS):
    def __call__(self, request, *args, **kwargs):
        self.category = get_object_or_404(Category, slug=kwargs['slug'])
        return super(CategoryRSS, self).__call__(request, *args, **kwargs)

    def title(self):
        try:
            return ''.join([Setting.objects.get(name='site_title').value,
                            u' » ', self.category.name])
        except ObjectDoesNotExist:
            return ''

    def description(self):
        return self.category.description

    def link(self):
        return reverse('lbe:category_rss', args=[self.category.slug])

    def items(self):
        return (Article.objects.filter(is_published=True, is_standalone=False,
                                       category=self.category)[:10])


class ArticleCommentsRSS(Feed):
    def __call__(self, request, *args, **kwargs):
        self.article = get_object_or_404(Article, slug=kwargs['slug'],
                                         is_published=True)
        return (super(ArticleCommentsRSS, self)
                .__call__(request, *args, **kwargs))

    def title(self):
        return ''.join([self.article.title, u' » ', _('comments')])

    def description(self):
        return _('Comments')

    def link(self):
        return reverse('lbe:article_comments_rss', args=[self.article.slug])

    def items(self):
        return (Comment.objects
                .filter(article=self.article, is_approved=True)
                .order_by('-created')[:25])

    def item_title(self, item):
        return item.user_name

    def item_description(self, item):
        return item.get_content()

    def item_pubdate(self, item):
        return item.created


def e404(request):
    return render(request, 'lbe/404.html', get_aside_content(), status=404)
