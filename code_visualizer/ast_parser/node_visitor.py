#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Visitor that iterates over the syntax-tree of a python code-string,
and selectivly visits a node based on registered interested parties.
"""
import ast
from collections import namedtuple

from .node_utils import get_children_parent


StackItem = namedtuple('StackItem', ['parent', 'node'])


class NodeVisitor(object):
    """Visitor that selectivly visits a syntax-tree"""
    def __init__(self):
        self.visitors = []

    def register_visitor(self, visit_criteria):
        """Add criteria to visitation-criterias"""
        self.visitors.append(visit_criteria)

    def visit(self, node_tree, visitors=None, parent=None):
        """Selectivly visit the syntax-tree with the registered visitors"""
        if visitors is None:
            visitors = self.visitors

        current_stack = [StackItem(parent=parent, node=node_tree)]

        while current_stack:
            node_parents, node = current_stack.pop(0)

            visitors_interested_in_children = []
            for visitor in visitors:
                if visitor.is_interested_in_node(node_parents, node):
                    visitor.visit_node(node_parents, node)
                if visitor.is_interested_in_children(node_parents, node):
                    visitors_interested_in_children.append(visitor)

            if visitors_interested_in_children:
                child_nodes_parent = get_children_parent(node, node_parents)
                for child in ast.iter_child_nodes(node):
                    self.visit(
                        child,
                        visitors_interested_in_children,
                        child_nodes_parent
                    )
