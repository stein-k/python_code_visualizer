#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import ast

from ast_parser.node_visitor import NodeVisitor
from ast_parser.node_filter import Criteria
from ast_parser.handlers.import_handler import ImportHandler

import_handler = ImportHandler()

class ImportFilter(Criteria):
    def is_interested_in_children(self, node_parents, node):
        return True

    def is_interested_in_node(self, node_parents, node):
        return isinstance(node, (ast.Import, ast.ImportFrom))

    def visit_node(self, node_parents, node):
        handle_node(node)


def handle_node(node):
    print(import_handler.handle(node))

def main(path):
    with open(path) as python_file:
        python_file_as_string = python_file.read()

    ast_tree = ast.parse(python_file_as_string)

    import_visitor = NodeVisitor()
    import_visitor.register_visitor(ImportFilter())
    import_visitor.visit(ast_tree)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("{0} <path to directory>".format(sys.argv[0]))