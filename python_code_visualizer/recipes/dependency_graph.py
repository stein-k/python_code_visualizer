#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Creates a dependency-graph from a directory of python files
which it writes to files.

Run from python_code_visualizer with "python[3] -m python_code_visualizer.recipes.dependency_graph"
"""
from __future__ import print_function

import ast
import collections
import os
import sys

from python_code_visualizer.ast_parser.node_filter import Criteria
from python_code_visualizer.ast_parser.node_visitor import NodeVisitor
from python_code_visualizer.ast_parser.parsers.import_parser import ImportParser
from python_code_visualizer.utils import path_walker


class _ImportFilter(Criteria):
    """Filter which visits all Import-nodes."""

    def __init__(self):
        self.module_imports = []
        self.import_parser = ImportParser()

    def wants_to_visit_descendants(self, node_parents, node):
        return True

    def handle_node(self, node_parents, node):
        """Adds the import to list of seen imports.

        :param node_parents: String of node parents
        :param node; Current node
        """
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for import_statement in self.import_parser.parse(node):
                what = import_statement.get('what_to_import')
                self.module_imports.append(what)


def dependency_graph(path):
    """
    Iterates over files in path and adds the relation
    between module and imports to a list, as well
    as the relation between module and file-path.

    :param path: path to create dependency graph for.
    """

    import_filter = _ImportFilter()
    node_visitor = NodeVisitor(import_filter)

    all_modules = set()
    file_paths = set()
    m2m_relations = set()
    m2p_relations = set()

    for file_path, file_name in path_walker.get_directory_structure(path):
        full_path = os.path.join(file_path, file_name)
        with open(full_path) as python_file:
            python_file_as_string = python_file.read()

        ast_tree = ast.parse(python_file_as_string)
        import_filter.module_imports = []
        node_visitor.visit(ast_tree)

        current_module = os.path.splitext(file_name)[0]
        file_paths.add(full_path)
        m2p_relations.add((current_module, full_path))
        all_modules.add(current_module)
        for imported_module in import_filter.module_imports:
            all_modules.add(imported_module)
            m2m_relations.add((current_module, imported_module))
    return all_modules, file_paths, m2m_relations, m2p_relations


def write_dependency_graph(input_path, output_path=''):
    """Writes the dependency graph to a set of files

    :param input_path: path to create dependency-graph for
    :param output_path: path to write write result to
    """
    (
        all_modules,
        file_paths,
        m2m_relations,
        m2p_relations) = dependency_graph(path=input_path)

    output = [
        ('modules.csv', all_modules),
        ('file_paths.csv', file_paths),
        ('m2m_relations.csv', m2m_relations),
        ('m2p_relations.csv', m2p_relations)
    ]

    for output_file_name, data in output:
        output_full_path = os.path.join(output_path, output_file_name)
        with open(output_full_path, 'w') as output_file:
            for line in data:
                if isinstance(line, str):
                    output_file.write(line + '\n')
                elif isinstance(line, collections.Iterable):
                    output_file.write(','.join(line) + '\n')
                else:
                    print('line intended for {0} unexpected: ({1})'.format(
                        output_full_path, type(line)))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if len(sys.argv) == 3:
            write_dependency_graph(
                input_path=sys.argv[1],
                output_path=sys.argv[2])
        else:
            write_dependency_graph(
                input_path=sys.argv[1])
    else:
        print(("{0} "
               "<path to INPUT-directory> "
               "<optional OUTPUT-directory>").format(sys.argv[0]))