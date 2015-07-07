#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prints the structure of a python file as indented node-names.
"""
import sys
import ast

from ast_parser.node_visitor import NodeVisitor
from ast_parser.node_filter import Criteria
from ast_parser.node_utils import get_node_name


class AllNameFilter(Criteria):
    """Filter which visits all nodes"""
    def wants_to_visit_descendants(self, node_parents, node):
        return True

    def wants_to_handle_node(self, node_parents, node):
        return True

    def handle_node(self, node_parents, node):
        """Prints the name of a node, indented one space per parent"""
        spacing = len(node_parents.split("."))*" " if node_parents else ""
        print("{0}{1}".format(spacing, get_node_name(node)))


def print_all_names(path_to_python_file):
    with open(path_to_python_file) as python_file:
        python_file_as_string = python_file.read()

    ast_tree = ast.parse(python_file_as_string)

    node_visitor = NodeVisitor()
    all_name_filter = AllNameFilter()
    node_visitor.register_filter(all_name_filter)
    node_visitor.visit(ast_tree)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        print_all_names(path_to_python_file=sys.argv[1])
    else:
        print('{} <path to python file>'.format(sys.argv[0]))
