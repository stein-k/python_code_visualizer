from python_code_visualizer.ast_parser.filters.if_name_main import IfMainFilter


def test_without_main(without_main):
    if_main_filter = IfMainFilter()

    for node in without_main:
        if_main_filter.handle_node(node_parents=None, node=node)
    assert if_main_filter.main_body == []
