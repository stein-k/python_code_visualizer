#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
from collections import namedtuple


DEPTH_FIRST = 0
BREADTH_FIRST = 1
StackItem = namedtuple('StackItem', ['parent', 'node'])


def visit(node_tree, ordering=DEPTH_FIRST):
    current_stack = [StackItem(parent='', node=node_tree)]

    while len(current_stack) > 0:
        node_parent, node = current_stack.pop(0)

        children_parent = get_children_parent(node, node_parent)

        children = [
            StackItem(parent=children_parent, node=child)
            for child
            in ast.iter_child_nodes(node)
        ]
        if ordering == DEPTH_FIRST:
            current_stack = children + current_stack
        else:
            current_stack = current_stack + children
        yield node_parent, node

def get_node_name(node):
    return node.name if hasattr(node, 'name') and node.name else type(node).__name__

def get_children_parent(node, node_parent):
    return '' if isinstance(node, ast.Module) else '.'.join([node_parent, get_node_name(node)])