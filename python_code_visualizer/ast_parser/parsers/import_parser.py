# -*- coding: utf-8 -*-
"""
Handles Import-nodes and ImportFrom-nodes in an AST
"""
import ast

from python_code_visualizer.ast_parser.parsers.interface import ParserInterface


class ParsedImport(object):
    def __init__(self, import_origin, name, asname, number_of_trailing_dots):
        self.where_to_import_from = import_origin
        self.what_to_import = name
        self.alias = asname
        self.name = asname if asname else name
        self.number_of_trailing_dots = number_of_trailing_dots
        if self.where_to_import_from:
            self.import_path = '{0}.{1}'.format(self.where_to_import_from, self.what_to_import)
        else:
            self.import_path = '{0}'.format(self.what_to_import)

    def get_relative_path(self):
        return '.' * self.number_of_trailing_dots + self.import_path


class ImportParser(ParserInterface):
    """Return a list of ParsedImport instances"""

    def parse(self, node):
        """Return ParsedImport for each imported name in node

        :param node: a supported node
        :type node: ast.Import, ast.ImportFrom

        :return: List of imports parsed from import node
        :rtype List[ParsedImport]
        """
        if isinstance(node, ast.ImportFrom):
            import_origin = node.module
            number_of_trailing_dots = node.level
        else:
            import_origin = None
            number_of_trailing_dots = 0
        return [
            ParsedImport(import_origin, name.name, name.asname, number_of_trailing_dots)
            for name in node.names
        ]

    @property
    def supported_types(self):
        """
        class Import(names)
        class ImportFrom(module, names, level)
        """
        return ast.Import, ast.ImportFrom
