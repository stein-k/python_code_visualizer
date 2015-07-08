# -*- coding: utf-8 -*-
"""
Visitor that iterates over the syntax-tree of a python code-string,
and selectivly visits a node based on registered interested parties.
"""
import ast
from collections import namedtuple

from .node_utils import get_children_parent


StackItem = namedtuple('StackItem', ['ascendants', 'node'])


class NodeVisitor(object):
    """Visitor that selectively visits a syntax-tree"""
    def __init__(self):
        self.filters = []

    def register_filter(self, filter_criteria):
        """Add criteria to visitation-criteria"""
        self.filters.append(filter_criteria)

    def visit(self, node_tree, filters=None, ascendants=None):
        """Selectively visit the syntax-tree with the registered visitors"""
        if filters is None:
            filters = self.filters

        current_stack = [StackItem(ascendants=ascendants, node=node_tree)]

        while current_stack:
            node_ascendants, node = current_stack.pop(0)

            active_filters = []
            for node_filter in filters:
                node_filter.handle_node(node_ascendants, node)
                if node_filter.wants_to_visit_descendants(node_ascendants, node):
                    active_filters.append(node_filter)

            if active_filters:
                child_ancestors = get_children_parent(node_ascendants, node)
                for child in ast.iter_child_nodes(node):
                    self.visit(
                        node_tree=child,
                        filters=active_filters,
                        ascendants=child_ancestors
                    )
