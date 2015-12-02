# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
import random
import string
from django.utils import lorem_ipsum


def make_tree(items):
    tree = []
    for item in items:
        item.children = []
        item.level = 1
        if item.parent_id is None:
            tree.append(item)
        else:
            try:
                parent = [p for p in items if p.id == item.parent_id][0]
                parent.children.append(item)
                item.level = parent.level + 1
            except ValueError:
                tree.append(item)
    return tree


def make_flat_tree(items):
    for item in items:
        item.path = str(item.id).rjust(8, '0')
        item.level = 1
        # ORM doesn't allow to use item.parent.path
        if item.parent_id is not None:
            parent = [p for p in items if p.id == item.parent_id][0]
            item.path = parent.path + item.path
            item.level = parent.level + 1
    return sorted(items, key=lambda x: x.path)


def random_char_seq(len=24):
    return ''.join(random.choice(string.ascii_letters) for i in range(len))


def random_string(len=24):
    token_len = int(len / 4)
    return ' '.join([random_char_seq(token_len),
                     lorem_ipsum.sentence()[:len - token_len - 1]])


def random_text(paragraphs=1):
    return ''.join([random_char_seq(24), ' '] +
                   lorem_ipsum.paragraphs(paragraphs))
