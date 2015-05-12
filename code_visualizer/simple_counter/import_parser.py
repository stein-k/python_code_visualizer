#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


_imports_on_one_line = re.compile('(?:from )?(?P<module>[\w_\.]+ )?import (?P<imports>[\w_, ]+)')
_imports_with_parenthesis = re.compile('(?:from )?(?P<module>[\w_\.]+ )?import \((?P<imports>[\w_, \n]+)\)')


def get_import_statements(python_code_as_string):
    """
    {
        'module_providing_import': ['<name of import>'...],
    }
    """
    imports_found = [found_import for found_import in re.findall(_imports_on_one_line, python_code_as_string)]
    imports_found.extend([found_import for found_import in re.findall(_imports_with_parenthesis, python_code_as_string)])
    #imports_found are now a list of ('imported from where', 'imported names')

    imports_map = {}
    for from_module, imported_objects in imports_found:
        module_key = from_module.strip()
        imported_objects.replace("\n", "")
        imports = imports_map.get(module_key, [])
        imports.extend([imported_module.strip() for imported_module in imported_objects.split(",")])
        imports_map[module_key] = imports

    return imports_map