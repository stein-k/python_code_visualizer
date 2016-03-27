# -*- coding: utf-8 -*-
"""
Visitor that iterates over the syntax-tree of a python code-string,
and notifies filters of individual code-elements seen.
"""
import ast
from collections import namedtuple

from .node_utils import get_children_parent


StackItem = namedtuple('StackItem', ['ascendants', 'node'])


class NodeVisitor(object):
    def __init__(self, initial_filter=None):
        """Visitor that selectively visits a syntax-tree.

        :param initial_filter: filter for this visitor
        :type initial_filter: Criteria
        """

        if initial_filter is None:
            self.filters = []
        else:
            self.filters = [initial_filter]

    def register_filter(self, filter_criteria):
        """Add criteria to visitation-criteria

        :param filter_criteria: filter for this visitor
        :type filter_criteria: Criteria
        """
        self.filters.append(filter_criteria)

    def visit(self, node_tree, filters=None, ascendants=None):
        """
        Selectively visit the syntax-tree with the registered visitors,
        and allow filters to handle code-elements they are interested in
        """
        if filters is None:
            filters = self.filters

        current_stack = [StackItem(ascendants=ascendants, node=node_tree)]

        while current_stack:
            node_ascendants, node = current_stack.pop(0)

            active_filters = []
            for node_filter in filters:
                node_filter.handle_node(
                    node_parents=node_ascendants,
                    node=node)
                if node_filter.wants_to_visit_descendants(
                        node_ascendants,
                        node):
                    active_filters.append(node_filter)

            if active_filters:
                child_ancestors = get_children_parent(node_ascendants, node)
                for child in ast.iter_child_nodes(node):
                    self.visit(
                        node_tree=child,
                        filters=active_filters,
                        ascendants=child_ancestors
                    )
