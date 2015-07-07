#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prints the names available in the global scope for a given module

Run from code_visualizer with "python[3] -m recipes.get_module_names"
"""
import sys
import ast

from ast_parser.node_visitor import NodeVisitor
from ast_parser.node_filter import Criteria

from ast_parser.handlers import __all__ as all_handlers


class GenericFilter(Criteria):
    """Filter which visits all top-level nodes"""
    def is_interested_in_children(self, node_parents, node):
        return node_parents is None

    def is_interested_in_node(self, node_parents, node):
        return True

    def visit_node(self, node_parents, node):
        handle_node(node)


_names = []


def handle_node(node):
    """Adds the name of the node to the list of seen names"""
    for handler in all_handlers:
        handler_instance = handler()
        if type(node) in handler_instance.supported_types():
            node_list = handler_instance.handle(node)
            _names.extend(
                [node_element.get('name') for node_element in node_list]
            )


def print_module_names(path_to_python_file):
    """
    Prints the path to the python file
    and a list of the names accessible in the module
    """
    with open(path_to_python_file) as python_file:
        python_file_as_string = python_file.read()

    ast_tree = ast.parse(python_file_as_string)

    import_visitor = NodeVisitor()
    import_visitor.register_visitor(GenericFilter())
    import_visitor.visit(ast_tree)
    print("{0} - {1}".format(path_to_python_file, _names))

if __name__ == '__main__':
    if len(sys.argv) == 2:
        print_module_names(path_to_python_file=sys.argv[1])
    else:
        print("{0} <path to python file>".format(sys.argv[0]))
