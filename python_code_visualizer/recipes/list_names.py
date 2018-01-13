#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prints the structure of a python file as indented node-names.

Run from python_code_visualizer with "python[3] -m python_code_visualizer.recipes.list_names"
"""
from __future__ import print_function

import ast
import sys

from python_code_visualizer.ast_parser.node_filter import Criteria
from python_code_visualizer.ast_parser.node_utils import get_node_name
from python_code_visualizer.ast_parser.node_visitor import NodeVisitor


class _AllNameFilter(Criteria):
    """Filter which visits all nodes"""

    def handle_node(self, node_parents, node):
        """Prints the name of a node, indented one space per parent

        :param node_parents: string of node parents
        :param node: current node
        """
        spacing = len(node_parents.split('.')) * ' ' if node_parents else ''
        print('{0}{1}'.format(spacing, get_node_name(node)))


def print_all_names(path_to_python_file):
    """
    Prints a list of the names accessible in the module

    :param path_to_python_file: path of python file to print module names for
    """
    with open(path_to_python_file) as python_file:
        python_file_as_string = python_file.read()

    ast_tree = ast.parse(python_file_as_string)

    node_visitor = NodeVisitor(_AllNameFilter())
    node_visitor.visit(ast_tree)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        print_all_names(path_to_python_file=sys.argv[1])
    else:
        print('{0} <path to python file>'.format(sys.argv[0]))
