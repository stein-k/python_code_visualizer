# -*- coding: utf-8 -*-
"""
Handles Import-nodes and ImportFrom-nodes in an AST
"""
import ast

from .interface import HandlerInterface


class ImportHandler(HandlerInterface):
    """Return a dict of information about an import
        {
            'where_to_import_from': '<where_to_import_from>',
            'what_to_import': '<what_to_import>',
            'alias': '<alias>',
            'name': '<name>',
            'level': <level>
        }
        """
    def handle(self, node):
        """Return import dict

        :param node: a supported node
        :type node: ast.Import, ast.ImportFrom

        :return: dictionary from import node
        """
        if isinstance(node, ast.ImportFrom):
            import_origin = node.module
            import_level = node.level
        else:
            import_origin = None
            import_level = 0
        return [
            {
                'where_to_import_from': import_origin,
                'what_to_import': name.name,
                'alias': name.asname,
                'name': name.asname if name.asname else name.name,
                'level': import_level
            } for name in node.names]

    @property
    def supported_types(self):
        """
        class Import(names)
        class ImportFrom(module, names, level)
        """
        return ast.Import, ast.ImportFrom
