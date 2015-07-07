#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prints the structure of a python file as indented node-names.
"""
import ast

from ast_parser.node_visitor import NodeVisitor
from ast_parser.node_filter import Criteria
from ast_parser.node_utils import get_node_name


class GenericFilter(Criteria):
    """Filter which visits all nodes"""
    def wants_to_visit_descendants(self, node_parents, node):
        return True

    def wants_to_handle_node(self, node_parents, node):
        return True

    def handle_node(self, node_parents, node):
        handle_node(node_parents, node)


def handle_node(node_parents, node):
    """Prints the name of a node, indented one space per parent"""
    spacing = len(node_parents.split("."))*" " if node_parents else ""
    print("{0}{1}".format(spacing, get_node_name(node)))


with open("utils/path_walker.py") as python_file:
    python_file_as_string = python_file.read()

    ast_tree = ast.parse(python_file_as_string)

    import_visitor = NodeVisitor()
    import_visitor.register_filter(GenericFilter())
    import_visitor.visit(ast_tree)
