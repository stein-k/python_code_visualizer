from python_code_visualizer.recipes.dependency_graph import dependency_graph


def test_relative_imports(test_projects, project_path):
    code_with_relative_imports = test_projects['relative_imports']
    project_modules, file_paths, m2m_relations, m2p_relations = dependency_graph(code_with_relative_imports)

    expected_project_modules_and_paths = {
        'main_module': project_path + '/tests/data/relative_imports/main_module.py',
        '__init__': project_path + '/tests/data/relative_imports/__init__.py',
        'library.__init__': project_path + '/tests/data/relative_imports/library/__init__.py',
        'library.module_a': project_path + '/tests/data/relative_imports/library/module_a.py',
        'library.module_b': project_path + '/tests/data/relative_imports/library/module_b.py',
        'library.module_c': project_path + '/tests/data/relative_imports/library/module_c.py',
    }
    expected_m2m_relations = {
        ('main_module', 'library.module_a'),
        ('library.module_a', 'library.module_b.foo'),
        ('library.module_a', 'library.module_c.ggg'),
    }

    assert set(project_modules) == set(expected_project_modules_and_paths.keys())
    assert set(file_paths) == set(expected_project_modules_and_paths.values())
    assert set(m2m_relations) == expected_m2m_relations
    assert set(m2p_relations) == set(expected_project_modules_and_paths.items())
