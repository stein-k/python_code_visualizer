#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main class that prints the python files of a directory and sub-directories
"""
from __future__ import print_function

import argparse
import os
from pprint import pprint

from recipes.get_entry_points import get_main_in_string
from recipes.get_imports import get_imports_in_string
from recipes.get_module_names import get_module_names_in_string
from utils.path_walker import get_directory_structure


def main(input_base_path):
    """
    Iterates over found python files and prints file-path and file-name
    :param input_base_path: Path to analyze
    :type input_base_path: str

    :return: Dictionary of analyzed files and the result
    :rtype; dict
    """
    big_dict = {}
    for file_path, file_name in get_directory_structure(input_base_path):
        path_to_python_file = os.path.join(file_path, file_name)
        local_dict = {}
        with open(path_to_python_file) as python_file:
            python_file_as_string = python_file.read()

        entry_points = get_main_in_string(python_file_as_string)
        local_dict['entry_points'] = entry_points

        list_of_imports = get_imports_in_string(python_file_as_string)
        imported_names = [name for _, name in list_of_imports]
        local_dict['imports'] = list_of_imports

        local_names = get_module_names_in_string(python_file_as_string)
        local_names = [
            local_name
            for local_name
            in local_names
            if local_name
            not in imported_names]
        local_dict['local_names'] = local_names
        big_dict[path_to_python_file] = local_dict
    return big_dict


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Visualize dependencies and structure of python code')

    parser.add_argument('--output_dir', help='The directory where files are created.')
    parser.add_argument('input_dir', help='The base path for the code to visualize.')

    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir
    output = main(input_dir)
    pprint(output)
