import ast
import os
from textwrap import dedent

import pytest

TEST_PATH = os.path.dirname(os.path.abspath(__file__))
TEST_CODE_PATH = os.path.join(TEST_PATH, 'data')
PROJECT_PATH = os.path.dirname(TEST_PATH)


@pytest.fixture
def project_path():
    return PROJECT_PATH


@pytest.fixture
def test_projects():
    _test_projects = {}
    for project in os.listdir(TEST_CODE_PATH):
        _test_projects[project] = os.path.join(TEST_CODE_PATH, project)
    return _test_projects


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
