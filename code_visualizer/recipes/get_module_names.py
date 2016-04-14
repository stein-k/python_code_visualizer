#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prints the names available in the global scope for a given module

Run from code_visualizer with "python[3] -m recipes.get_module_names"
"""
from __future__ import print_function

import ast
import sys

from ast_parser.node_filter import Criteria
from ast_parser.node_visitor import NodeVisitor
from ast_parser.parsers import assignment_parser, class_parser, function_parser, import_parser

_all_parsers = [assignment_parser.AssignmentParser,
                class_parser.ClassParser,
                function_parser.FunctionParser,
                import_parser.ImportParser
                ]


class _ModuleNameFilter(Criteria):
    """Filter which visits all top-level nodes"""

    def __init__(self):
        self.names = []

    def wants_to_visit_descendants(self, node_parents, node):
        return node_parents is None

    def handle_node(self, node_parents, node):
        """Adds the name of the node to the list of seen names

        :param node_parents: string of node parents
        :param node: current node
        """
        for paser in _all_parsers:
            parser_instance = paser()
            if isinstance(node, parser_instance.supported_types):
                node_list = parser_instance.parse(node)
                self.names.extend(
                    [node_element.get('name') for node_element in node_list]
                )


def print_module_names(path_to_python_file):
    """
    Prints the path to the python file
    and a list of the names accessible in the module

    :param path_to_python_file: path of python file to print module names for
    """
    with open(path_to_python_file) as python_file:
        python_file_as_string = python_file.read()

    ast_tree = ast.parse(python_file_as_string)

    module_name_filter = _ModuleNameFilter()
    node_visitor = NodeVisitor(module_name_filter)
    node_visitor.visit(ast_tree)
    print('{0} - {1}'.format(path_to_python_file, module_name_filter.names))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        print_module_names(path_to_python_file=sys.argv[1])
    else:
        print('{0} <path to python file>'.format(sys.argv[0]))
