from python_code_visualizer.ast_parser.node_filter import Criteria
from python_code_visualizer.ast_parser.parsers.import_parser import ImportParser


class ImportFilter(Criteria):
    """Filter which visits all Import-nodes"""

    def __init__(self):
        self.module_imports = []
        self.import_parser = ImportParser()

    def handle_node(self, node_parents, node):
        """Adds the import to the list of seen imports

        :param node_parents: string of node parents
        :param node: current node
        """
        if isinstance(node, self.import_parser.supported_types):
            for import_statement in self.import_parser.parse(node):
                self.module_imports.append(import_statement)
