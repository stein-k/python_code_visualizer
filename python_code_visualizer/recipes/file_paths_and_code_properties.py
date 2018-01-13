#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main class that prints the python files of a directory and sub-directories
"""
from __future__ import print_function

import os

from python_code_visualizer.recipes.get_entry_points import get_main_in_string
from python_code_visualizer.recipes.get_imports import get_imports_in_string
from python_code_visualizer.recipes.get_module_names import get_module_names_in_string
from python_code_visualizer.utils.path_walker import get_directory_structure


def as_dict(input_base_path):
    """
    Iterates over found python files and prints file-path and file-name
    :param input_base_path: Path to analyze
    :type input_base_path: str

    :return: Dictionary of analyzed files and the result
    :rtype; dict
    """
    file_paths_to_code_properties = {}
    for file_path, file_name in get_directory_structure(input_base_path):
        path_to_python_file = os.path.join(file_path, file_name)
        code_properties = {}
        with open(path_to_python_file) as python_file:
            python_file_as_string = python_file.read()

        entry_points = get_main_in_string(python_file_as_string)
        code_properties['entry_points'] = entry_points

        list_of_imports = get_imports_in_string(python_file_as_string)
        imported_names = [name for _, name in list_of_imports]
        code_properties['imports'] = list_of_imports

        local_names = get_module_names_in_string(python_file_as_string)
        local_names = [
            local_name
            for local_name
            in local_names
            if local_name
            not in imported_names]
        code_properties['local_names'] = local_names
        file_paths_to_code_properties[path_to_python_file] = code_properties
    return file_paths_to_code_properties
