import ast

from ast_parser.node_visitor import NodeVisitor
from ast_parser.node_filter import Criteria
from ast_parser.node_utils import get_node_name


class GenericFilter(Criteria):
    def is_interested_in_children(self, node_parents, node):
        return True

    def is_interested_in_node(self, node_parents, node):
        return True

    def visit_node(self, node_parents, node):
        handle_node(node_parents, node)


def handle_node(node_parents, node):
    spacing = len(node_parents.split("."))*" " if node_parents else ""
    print("{0}{1}".format(spacing, get_node_name(node)))


with open("/home/stein/Code/skunk/python_code_visualizer/code_visualizer/utils/path_walker.py") as python_file:
    python_file_as_string = python_file.read()

    ast_tree = ast.parse(python_file_as_string)

    import_visitor = NodeVisitor()
    import_visitor.register_visitor(GenericFilter())
    import_visitor.visit(ast_tree)
