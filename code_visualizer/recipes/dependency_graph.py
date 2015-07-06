#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import ast

from ast_parser.node_visitor import NodeVisitor
from ast_parser.node_filter import Criteria
from ast_parser.handlers.import_handler import ImportHandler
from utils import path_walker


class ImportFilter(Criteria):
    def is_interested_in_children(self, node_parents, node):
        return True

    def is_interested_in_node(self, node_parents, node):
        return isinstance(node, (ast.Import, ast.ImportFrom))

    def visit_node(self, node_parents, node):
        handle_node(node)


import_handler = ImportHandler()
module_imports = []
all_modules = set()
file_paths = set()
m2m_relations = set()
m2p_relations = set()


def handle_node(node):
    global module_imports
    for import_statement in import_handler.handle(node):
        what = import_statement.get('what_to_import')
        module_imports.append(what)


def dependency_graph(path):
    global module_imports

    import_visitor = NodeVisitor()
    import_visitor.register_visitor(ImportFilter())

    for file_path, file_name in path_walker.get_directory_structure(path):
        full_path = os.path.join(file_path, file_name)
        with open(full_path) as python_file:
            python_file_as_string = python_file.read()

        ast_tree = ast.parse(python_file_as_string)
        import_visitor.visit(ast_tree)
        # module_imports now contains list of modules current file imports

        current_module = os.path.splitext(file_name)[0]
        file_paths.add(full_path)
        m2p_relations.add((current_module, full_path))
        all_modules.add(current_module)
        for imported_module in module_imports:
            all_modules.add(imported_module)
            m2m_relations.add((current_module, imported_module))

        # empty set of modules to prepare to process next file
        module_imports = []


if __name__ == '__main__':
    if len(sys.argv) == 2:
        dependency_graph(sys.argv[1])
        base_path = '/home/stein/Code/skunk/visualizer'
        output = [
            ('modules.csv', all_modules),
            ('filepaths.csv', file_paths),
            ('m2m_relations.csv', m2m_relations),
            ('m2p_relations.csv', m2p_relations)
        ]
        for output_file_name, data in output:
            output_full_path = os.path.join(base_path, output_file_name)
            with open(output_full_path, 'w') as output:
                for line in data:
                    if isinstance(line, str):
                        output.write(line+'\n')
                    else:
                        output.write(','.join(line)+'\n')
    else:
        print("{0} <path to directory>".format(sys.argv[0]))
