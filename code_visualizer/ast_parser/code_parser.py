#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
from collections import namedtuple


class CodeParser(object):
    """
    Returns a structure of the python code as below:
    {
        'name' : {
            'type': '<type>',
            'line_number': XXX,
            'col_number' : YYY,
            'structure' : {},
            'children' : {
                'name' : {
                    'type': '<type>',
                    'line_number': XXX,
                    'col_number' : YYY,
                    'structure' : {},
                    'children' : {
                    }
                }
            }
        }
    }

    Currently supported syntax elements:
        Module, Import, ImportFrom, ClassDef, FunctionDef, Assign

    """

    def parse_python_code(self, python_code_as_string):

        result = {
            '': {
                'type': 'Module',
                'line_number': -1,
                'col_number': -1,
                'structure': {},
                'children': {}
            }
        }
        syntax_tree = ast.parse(python_code_as_string)

        current_stack = []
        StackItem = namedtuple('StackItem', ['lookup_path', 'node'])
        current_stack.extend(
            [
                StackItem(lookup_path='', node=node)
                for node
                in ast.iter_child_nodes(syntax_tree)
            ]
        )

        while len(current_stack) > 0:
            lookup_path, node = current_stack.pop(0)

            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                for import_statement in self._handle_import(node):
                    update_dict = self._format_update_dict(node, import_statement)
                    update_dict.update(type='import')
                    self._insert_into_tree(result, lookup_path, update_dict)

            if isinstance(node, ast.FunctionDef):
                update_dict = self._format_update_dict(node, self._handle_function(node))
                self._insert_into_tree(result, lookup_path, update_dict)

            if isinstance(node, ast.ClassDef):
                update_dict = self._format_update_dict(node, self._handle_class(node))
                self._insert_into_tree(result, lookup_path, update_dict)
                child_lookup_path = '.'.join([lookup_path, update_dict['structure']['name']])
                current_stack.extend(
                    [
                        StackItem(lookup_path=child_lookup_path, node=child)
                        for child
                        in ast.iter_child_nodes(node)
                    ]
                )

            if isinstance(node, ast.Assign):
                for assignment in self._handle_assignment(node):
                    update_dict = self._format_update_dict(node, assignment)
                    self._insert_into_tree(result, lookup_path, update_dict)

        return result

    def _format_update_dict(self, node, structure):
        return {
            'type': type(node).__name__,
            'line_number': node.lineno,
            'col_number': node.col_offset,
            'structure': structure,
            'children': {}
        }

    def _insert_into_tree(self, result_dict, leaf_lookup_path, update_dict):
        assert('name' in update_dict['structure'])

        node_update = {update_dict['structure']['name']: update_dict}

        current_branch = result_dict
        for path_item in leaf_lookup_path.split('.'):
            current_branch = current_branch.get(path_item).get('children')

        current_branch.update(node_update)

    def _handle_import(self, node):
        """
        {
            'where_to_import_from': '<where_to_import_from>',
            'what_to_import': '<what_to_import>',
            'alias': '<alias>',
            'name': '<name>'
        }
        """
        assert(isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom))
        return [
            {
                'where_to_import_from': node.module if isinstance(node, ast.ImportFrom) else None,
                'what_to_import': name.name,
                'alias': name.asname,
                'name': name.asname if name.asname else name.name
            } for name in node.names]

    def _handle_function(self, node):
        """Returns information about the parsed function
        {
            'name': '<name>',
            'args': [{
                        'name': '<arg_name>'
                    }],
            'vararg': '<vararg_name>',
            'kwarg': '<kwargs_name>',
            'defaults': [{
                            'line_number': XXXX,
                            'col_offset': YYYY,
                        }]
        }
        """
        assert(isinstance(node, ast.FunctionDef))
        return {
            'name': node.name,
            'line_number': node.lineno,
            'col_offset': node.col_offset,
            'vararg': node.args.vararg,
            'kwarg': node.args.kwarg,
            'args': [
                {'name': arg.id, 'line_number': arg.lineno, 'col_offset': arg.col_offset}
                for arg in node.args.args],
            'defaults': [
                {'value': default.id, 'line_number': default.lineno, 'col_offset': default.col_offset}
                for default in node.args.defaults]
        }

    def _handle_class(self, node):
        """
        {
            'name': '<name>',
            'bases': ['<base_name>'...]
        }
        """
        assert(isinstance(node, ast.ClassDef))
        return {
            'name': node.name,
            'bases': [base.id for base in node.bases]
        }

    def _handle_assignment(self, node):
        """
        {
            'name': '<name>',

        """
        assert(isinstance(node, ast.Assign))
        return [
            {
                'name': target.id
            }
            for target
            in node.targets
        ]

if __name__ == '__main__':
    code_parser = CodeParser()
    # filename = '/home/stein/Code/skunk/python_code_visualizer/code_visualizer/ast_parser/code_parser.py'
    filename = '/home/stein/Code/skunk/python_code_visualizer/repository/requests/requests/adapters.py'
    with open(filename, 'r') as python_code:
        res = code_parser.parse_python_code(python_code.read())

    from pprint import pprint
    pprint(res)
