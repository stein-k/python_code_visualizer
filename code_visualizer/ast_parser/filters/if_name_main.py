import ast

from ast_parser.node_filter import Criteria
from ast_parser.node_utils import get_node_name, get_node_value
from ast_parser.parsers.if_parser import IfParser


class IfMainFilter(Criteria):
    """
    Filter which visits "if __name__ == '__main__' statements
    """

    def __init__(self):
        self.main_body = []
        self.if_handler = IfParser()

    def wants_to_visit_descendants(self, node_parents, node):
        """Only visit top level nodes

        :param node_parents: string of parent-nodes
        :type node_parents: str

        :param node: current node
        :type node: ast.Ast

        :return True if children of node should be visited
        :return False if children of node should not be visited
        """
        return node_parents is None

    def handle_node(self, node_parents, node):
        """Adds node body to list of main-bodies if it matches the criteria.

        :param node_parents: string of node parents
        :param node: current node
        """
        if isinstance(node, self.if_handler.supported_types):
            node_dict = self.if_handler.parse(node)

            left, op, right = get_if_parts(node_dict)
            if is_name(left) and is_equal(op) and is_main(right):
                self.main_body.append(node)


def get_if_parts(node_dict):
    test = node_dict.get('test')
    if isinstance(test, ast.Compare):
        left_side = test.left
        comparator = test.ops[0]
        right_side = test.comparators[0]
        return left_side, comparator, right_side
    return None, None, None


def is_name(node):
    return isinstance(node, ast.Name) \
           and get_node_name(node) == '__name__'


def is_main(node):
    return isinstance(node, ast.Str) \
        and get_node_value(node) == '__main__'


def is_equal(node):
    return isinstance(node, ast.Eq)
