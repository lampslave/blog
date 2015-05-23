# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.forms.widgets import Textarea


class AdminCodeMirrorWidget(Textarea):

    class Media:
        js = ['lbe/codemirror/lib/codemirror.js',
              'lbe/codemirror/addon/mode/overlay.js',
              'lbe/codemirror/mode/xml/xml.js',
              'lbe/codemirror/mode/markdown/markdown.js',
              'lbe/codemirror/mode/gfm/gfm.js',
              'lbe/codemirror/mode/javascript/javascript.js',
              'lbe/codemirror/mode/css/css.js',
              'lbe/codemirror/mode/htmlmixed/htmlmixed.js',
              'lbe/codemirror/mode/python/python.js',
              'lbe/codemirror/mode/shell/shell.js',
              'lbe/codemirror/mode/meta.js',
              'lbe/codemirror-lbe.js',]
        css = {
            'all': ['lbe/codemirror/lib/codemirror.css',
                    'lbe/codemirror-lbe.css',]
        }

    def __init__(self, attrs=None):
        attrs = attrs or {}
        attrs['class'] = attrs.setdefault('class', '') + ' codemirror-widget'
        super(AdminCodeMirrorWidget, self).__init__(attrs=attrs)
