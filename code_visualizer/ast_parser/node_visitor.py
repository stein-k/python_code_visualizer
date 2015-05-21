#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
from collections import namedtuple

from .node_filter import PassThroughCriteria


DEPTH_FIRST = 0
BREADTH_FIRST = 1
StackItem = namedtuple('StackItem', ['parent', 'node'])
GENERATION_SEPARATOR = '.'


def visit(node_tree, ordering=DEPTH_FIRST, node_filter=None):
    current_stack = [StackItem(parent='', node=node_tree)]

    if not node_filter:
        node_filter = PassThroughCriteria()

    while len(current_stack) > 0:
        node_parents_types, node = current_stack.pop(0)

        children_parent = get_children_parent(node, node_parents_types)

        if node_filter.visit_children(node_parents_types=node_parents_types, node=node):
            children = [
                StackItem(parent=children_parent, node=child)
                for child
                in ast.iter_child_nodes(node)
            ]
            if ordering == DEPTH_FIRST:
                current_stack = children + current_stack
            else:
                current_stack = current_stack + children

        if node_filter.return_node(node_parents_types=node_parents_types, node=node):
            yield node_parents_types, node

def get_node_name(node):
    name = node.name if hasattr(node, 'name') and node.name else type(node).__name__
    if isinstance(name, ast.Name):
        name = name.id
    return name

def get_children_parent(node, node_parent):
    return '' \
        if isinstance(node, ast.Module) \
        else GENERATION_SEPARATOR.join([node_parent, get_node_name(node)])
