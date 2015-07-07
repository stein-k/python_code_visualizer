#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prints a list of imports for a given python-file.

Run from code_visualizer with "python[3] -m recipes.get_imports"
"""

import sys
import ast

from ast_parser.node_visitor import NodeVisitor
from ast_parser.node_filter import Criteria
from ast_parser.handlers.import_handler import ImportHandler


class ImportFilter(Criteria):
    def is_interested_in_children(self, node_parents, node):
        return True

    def is_interested_in_node(self, node_parents, node):
        return isinstance(node, (ast.Import, ast.ImportFrom))

    def visit_node(self, node_parents, node):
        handle_node(node)


import_handler = ImportHandler()
module_imports = []


def handle_node(node):
    for import_statement in import_handler.handle(node):
        what = import_statement.get('what_to_import')
        where = import_statement.get('where_to_import_from')
        if where:
            module_imports.append('{0}.{1}'.format(where, what))
        else:
            module_imports.append('{0}'.format(what))


def print_imports(path_to_python_file):
    with open(path_to_python_file) as python_file:
        python_file_as_string = python_file.read()

    ast_tree = ast.parse(python_file_as_string)

    import_visitor = NodeVisitor()
    import_visitor.register_visitor(ImportFilter())
    import_visitor.visit(ast_tree)
    print('{0} - {1}'.format(path_to_python_file, module_imports))

if __name__ == '__main__':
    if len(sys.argv) == 2:
        print_imports(path_to_python_file=sys.argv[1])
    else:
        print("{0} <path to python file>".format(sys.argv[0]))
