#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import ast

from ast_parser.node_visitor import NodeVisitor
from ast_parser.node_filter import Criteria
from ast_parser.node_utils import get_node_name


class GenericFilter(Criteria):
    def is_interested_in_children(self, node_parents, node):
        return node_parents is None

    def is_interested_in_node(self, node_parents, node):
        return True

    def visit_node(self, node_parents, node):
        parents = node_parents.split['.'] if node_parents else []
        tabs = "\t" * len(parents)
        print("{0}{1} - {2}".format(tabs, node_parents, get_node_name(node)))


def main(path):
    with open(path) as python_file:
        python_file_as_string = python_file.read()

    ast_tree = ast.parse(python_file_as_string)

    import_visitor = NodeVisitor()
    import_visitor.register_visitor(GenericFilter())
    import_visitor.visit(ast_tree)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("{0} <path to directory>".format(sys.argv[0]))