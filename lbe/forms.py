# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.forms import ModelForm, widgets as w
from django.utils.translation import ugettext as _
from pagedown.widgets import PagedownWidget
from lbe.models import Comment


class CommentForm(ModelForm):

    class Meta():
        model = Comment
        exclude = ['is_approved', 'created']
        widgets = {
            'article': w.HiddenInput, 'parent': w.HiddenInput,
            'content': PagedownWidget,
            'user_email': w.TextInput(attrs={'placeholder':
                                             _('for gravatar service only')})
        }
