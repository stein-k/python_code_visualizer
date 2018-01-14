import ast
import os
from textwrap import dedent

import pytest

TEST_PATH = os.path.dirname(os.path.abspath(__file__))
TEST_CODE_PATH = os.path.join(TEST_PATH, 'data')


@pytest.fixture
def test_code():
    test_projects = {}
    for project in os.listdir(TEST_CODE_PATH):
        test_projects[project] = os.path.join(TEST_CODE_PATH, project)
    return test_projects


@pytest.fixture
def without_main():
    code_string_without_main = dedent("""
    var = 'this is string'
    if var == 'some other string':
        return True
    elif var == '':
        return False
    else:
        return False
    """)
    ast_tree = ast.parse(code_string_without_main)
    return ast_tree.body
