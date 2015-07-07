#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Creates a dependency-graph from a directory of python files
which it writes to files.
"""
import sys
import os
import ast

from ast_parser.node_visitor import NodeVisitor
from ast_parser.node_filter import Criteria
from ast_parser.handlers.import_handler import ImportHandler
from utils import path_walker


class ImportFilter(Criteria):
    """Filter which visits all Import-nodes"""
    def is_interested_in_children(self, node_parents, node):
        return True

    def is_interested_in_node(self, node_parents, node):
        return isinstance(node, (ast.Import, ast.ImportFrom))

    def visit_node(self, node_parents, node):
        handle_node(node)


_import_handler = ImportHandler()
_module_imports = []
_all_modules = set()
_file_paths = set()
_m2m_relations = set()
_m2p_relations = set()


def handle_node(node):
    """Adds the import to list of seen imports"""
    for import_statement in _import_handler.handle(node):
        what = import_statement.get('what_to_import')
        _module_imports.append(what)


def dependency_graph(path):
    """
    Iterates over files in path and adds the relation
    between module and imports to a list, as well
    as the relation between module and file-path.
    """
    global _module_imports

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
        _file_paths.add(full_path)
        _m2p_relations.add((current_module, full_path))
        _all_modules.add(current_module)
        for imported_module in _module_imports:
            _all_modules.add(imported_module)
            _m2m_relations.add((current_module, imported_module))

        # empty set of modules to prepare to process next file
        _module_imports = []


if __name__ == '__main__':
    if len(sys.argv) == 2:
        dependency_graph(path=sys.argv[1])
        base_path = '/home/stein/Code/skunk/visualizer'
        output = [
            ('modules.csv', _all_modules),
            ('filepaths.csv', _file_paths),
            ('m2m_relations.csv', _m2m_relations),
            ('m2p_relations.csv', _m2p_relations)
        ]
        for output_file_name, data in output:
            output_full_path = os.path.join(base_path, output_file_name)
            with open(output_full_path, 'w') as output_file:
                for line in data:
                    if isinstance(line, str):
                        output_file.write(line+'\n')
                    else:
                        output_file.write(','.join(line)+'\n')
    else:
        print("{0} <path to directory>".format(sys.argv[0]))
