#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prints a list of files with common python entry-point:
if __name__ == '__main__':


Run from code_visualizer with "python[3] -m recipes.get_entry_points"
"""
from __future__ import print_function
import ast

import sys

from ast_parser.handlers.if_handler import IfHandler
from ast_parser.node_utils import get_node_name, get_node_value
from ast_parser.node_visitor import NodeVisitor
from ast_parser.node_filter import Criteria


class _IfMainFilter(Criteria):
    """
    Filter which visits "if __name__ == '__main__' statements
    """

    def __init__(self):
        self.has_main = False
        self.if_handler = IfHandler()

    def wants_to_visit_descendants(self, node_parents, node):
        return True

    def handle_node(self, node_parents, node):
        """
        Adds the module to modules_with_main
        if it has a main declaration.

        :param node_parents: string of node parents
        :param node: current node
        """
        if isinstance(node, self.if_handler.supported_types):
            left, op, right = self.get_if_parts(node)
            if _IfMainFilter.if_eq_main(left, op, right):
                self.has_main = True

    def get_if_parts(self, node):
        node_dict = self.if_handler.handle(node)
        test = node_dict.get('test')
        if isinstance(test, ast.Compare):
            left_side = test.left
            comparator = test.ops[0]
            right_side = test.comparators[0]
            return left_side, comparator, right_side
        return None, None, None

    @staticmethod
    def if_eq_main(left, op, right):
        if isinstance(left, ast.Name)\
                and get_node_name(left) == '__name__' \
                and isinstance(op, ast.Eq) \
                and isinstance(right, ast.Str) \
                and get_node_value(right) == '__main__':
            return True
        else:
            return False


def print_main(path_to_python_file):
    """Prints the path to the python file if it has a
    if __name__ == '__main__'
    at the root of the module.

    :param path_to_python_file: path of python file to print imports for
    """
    with open(path_to_python_file) as python_file:
        python_file_as_string = python_file.read()

    ast_tree = ast.parse(python_file_as_string)

    if_main_filter = _IfMainFilter()
    if_statement_visitor = NodeVisitor(if_main_filter)
    if_statement_visitor.visit(ast_tree)
    if if_main_filter.has_main:
        print('{0}'.format(path_to_python_file))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        print_main(path_to_python_file=sys.argv[1])
    else:
        print('{0} <path to python file>'.format(sys.argv[0]))
