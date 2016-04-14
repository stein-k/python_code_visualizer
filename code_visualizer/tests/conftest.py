import ast

import pytest


@pytest.fixture
def without_main():
    code_string_without_main = """
    var = 'this is string'
    if var == 'some other string':
        return True
    elif var == '':
        return False
    else:
        return False
    """
    ast_tree = ast.parse(code_string_without_main)
    return ast_tree.body