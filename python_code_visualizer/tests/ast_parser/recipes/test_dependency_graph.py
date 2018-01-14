from python_code_visualizer.recipes.dependency_graph import dependency_graph


def test_relative_imports(test_projects):
    code_with_relative_imports = test_projects['relative_imports']
    all_modules, file_paths, m2m_relations, m2p_relations = dependency_graph(code_with_relative_imports)

    expected_modules = ('main_module', '__init__', 'module_a', 'module_b')
    expected_file_paths = (
        'python_code_visualizer/tests/data/relative_imports/library/__init__.py',
        'python_code_visualizer/tests/data/relative_imports/library/module_a.py',
        'python_code_visualizer/tests/data/relative_imports/__init__.py',
        'python_code_visualizer/tests/data/relative_imports/main_module.py',
        'python_code_visualizer/tests/data/relative_imports/library/module_b.py',
    )
    expected_m2m_relations = (('main_module', 'library.module_a'),
                              ('module_a', 'library.module_b'),
                              )
