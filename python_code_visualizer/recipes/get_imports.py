#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prints a list of imports for a given python-file.

Run from python_code_visualizer with "python[3] -m python_code_visualizer.recipes.get_imports"
"""
from __future__ import print_function

import ast
import sys

from python_code_visualizer.ast_parser.filters.import_filter import ImportFilter
from python_code_visualizer.ast_parser.node_visitor import NodeVisitor


def get_imports_in_file(path_to_python_file):
    """Return the list of imports for a python file

    :param path_to_python_file: path of python file to return imports for
    :type path_to_python_file: str

    :return: List of import statement
    :rtype: List of str
    """
    with open(path_to_python_file) as python_file:
        python_file_as_string = python_file.read()
    return get_imports_in_string(python_file_as_string)


def get_imports_in_string(code_as_string):
    """Return the list of imports for python code.

    :param code_as_string: python code to return imports for
    :type code_as_string: str

    :return: List of import statement
    :rtype: List of str
    """
    ast_tree = ast.parse(code_as_string)

    import_filter = ImportFilter()
    import_visitor = NodeVisitor(import_filter)
    import_visitor.visit(ast_tree)
    return import_filter.module_imports


if __name__ == '__main__':
    if len(sys.argv) == 2:
        input_file = sys.argv[1]
        list_of_imports = get_imports_in_file(input_file)
        filtered_list_of_imports = [
            import_path for import_path, _ in list_of_imports
            ]
        print('{0} - {1}'.format(input_file, filtered_list_of_imports))
    else:
        print('{0} <path to python file>'.format(sys.argv[0]))
