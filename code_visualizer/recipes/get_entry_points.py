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

from ast_parser.filters.if_name_main import IfMainFilter
from ast_parser.node_visitor import NodeVisitor


def print_main(path_to_python_file):
    """Prints the path to the python file if it has a
    if __name__ == '__main__'
    at the root of the module.

    :param path_to_python_file: path of python file to print imports for
    """
    with open(path_to_python_file) as python_file:
        python_file_as_string = python_file.read()

    ast_tree = ast.parse(python_file_as_string)

    if_main_filter = IfMainFilter()
    if_statement_visitor = NodeVisitor(if_main_filter)
    if_statement_visitor.visit(ast_tree)
    if if_main_filter.main_body:
        print('{0} - at line {1}'.format(path_to_python_file, [m.lineno for m in if_main_filter.main_body]))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        print_main(path_to_python_file=sys.argv[1])
    else:
        print('{0} <path to python file>'.format(sys.argv[0]))
