#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prints a list of files with common python entry-point:
if __name__ == '__main__':


Run from python_code_visualizer with "python[3] -m python_code_visualizer.recipes.get_entry_points"
"""
from __future__ import print_function

import ast
import sys

from python_code_visualizer.ast_parser.filters.if_name_main import IfMainFilter
from python_code_visualizer.ast_parser.node_visitor import NodeVisitor


def get_main_in_file(path_to_python_file):
    """Return the list of :
    if __name__ == '__main__'
    from the root of the module.

    :param path_to_python_file: path of python file to get entry-points from.
    :type path_to_python_file: str

    :return: List of line-numbers where entry-point is present in code.
    :rtype: list of int
    """
    with open(path_to_python_file) as python_file:
        python_file_as_string = python_file.read()

        return get_main_in_string(python_file_as_string)


def get_main_in_string(code_as_string):
    """Return the list of :
    if __name__ == '__main__'
    from the root of the module.

    :param code_as_string: string representation of python code
    to get entry-points from.
    :type code_as_string: str

    :return: List of line-numbers where entry-point is present in code.
    :rtype: list of int
    """
    ast_tree = ast.parse(code_as_string)

    if_main_filter = IfMainFilter()
    if_statement_visitor = NodeVisitor(if_main_filter)
    if_statement_visitor.visit(ast_tree)
    if if_main_filter.main_body:
        return [m.lineno for m in if_main_filter.main_body]
    else:
        return []


if __name__ == '__main__':
    if len(sys.argv) == 2:
        input_file = sys.argv[1]
        list_of_mains = get_main_in_file(input_file)
        if list_of_mains:
            print('{0} - at line {1}'.format(input_file, list_of_mains))
        else:
            print('No main entry found in {0}'.format(input_file))
    else:
        print('{0} <path to python file>'.format(sys.argv[0]))
