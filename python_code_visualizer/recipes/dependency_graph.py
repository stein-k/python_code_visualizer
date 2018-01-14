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

from python_code_visualizer.ast_parser.filters.import_filter import ImportFilter
from python_code_visualizer.ast_parser.node_visitor import NodeVisitor
from python_code_visualizer.utils import path_walker


def _get_module_path_relative_to_project(project_path, module_file_path):
    relative_file_path = module_file_path[len(project_path):]
    without_leading_sep = relative_file_path.lstrip(os.sep)
    without_extension = os.path.splitext(without_leading_sep)[0]
    relative_module_path = without_extension.replace(os.path.sep, '.')
    return relative_module_path


def _normalize_imported_module_to_project(importer, imported_module):
    """
    >>> _normalize_imported_module_to_project('library.module_a', '.module_b')
    'library.module_b'
    >>> _normalize_imported_module_to_project('library.module_a', 'itertools')
    'itertools'
    >>> _normalize_imported_module_to_project('library.path_1.module_a', '..module_b')
    'library.module_b'
    >>> _normalize_imported_module_to_project('library.path_1.path_2.module_a', '...module_b')
    'library.module_b'

    :param importer: the module in which the import statement is found
    :type importer: str

    :param imported_module: the import statement joined by dots
    :type imported_module: str

    :return: the imported module normalized by the importing module's path
    :rtype: str
    """
    if not imported_module.startswith('.'):
        return imported_module
    importer_parts = importer.split('.')
    while imported_module.startswith('.'):
        importer_parts = importer_parts[:-1]
        imported_module = imported_module[1:]
    importer_parts.append(imported_module)
    return '.'.join(importer_parts)


def dependency_graph(project_path):
    """
    Iterates over files in path and adds the relation
    between module and imports to a list, as well
    as the relation between module and file-path.

    :param project_path: path to create dependency graph for.
    """

    import_filter = ImportFilter()
    node_visitor = NodeVisitor(import_filter)

    project_modules = set()
    file_paths = set()
    m2m_relations = set()
    m2p_relations = set()

    for file_path, file_name in path_walker.get_directory_structure(project_path):
        full_path = os.path.join(file_path, file_name)
        with open(full_path) as python_file:
            python_file_as_string = python_file.read()

        ast_tree = ast.parse(python_file_as_string)
        import_filter.module_imports = []
        node_visitor.visit(ast_tree)

        current_module = _get_module_path_relative_to_project(project_path, full_path)
        file_paths.add(full_path)
        m2p_relations.add((current_module, full_path))
        project_modules.add(current_module)
        for imported_module in import_filter.module_imports:
            normalized_imported_module = _normalize_imported_module_to_project(
                current_module,
                imported_module.get_relative_path())
            m2m_relations.add((current_module, normalized_imported_module))
    return project_modules, file_paths, m2m_relations, m2p_relations


def write_dependency_graph(input_path, output_path=''):
    """Writes the dependency graph to a set of files

    :param input_path: path to create dependency-graph for
    :param output_path: path to write write result to
    """
    (
        all_modules,
        file_paths,
        m2m_relations,
        m2p_relations) = dependency_graph(project_path=input_path)

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
