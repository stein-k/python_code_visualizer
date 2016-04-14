#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main class that prints the python files of a directory and sub-directories
"""
from __future__ import print_function

import argparse

from utils.path_walker import get_directory_structure


def main(input_base_path, output_path=None):
    """
    Iterates over found python files and prints file-path and file-name
    """
    for file_path, file_name in get_directory_structure(input_base_path):
        print(file_path, file_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Visualize dependencies and structure of python code')

    parser.add_argument('--output_dir', help='The directory where files are created.')
    parser.add_argument('input_dir', help='The base path for the code to visualize.')

    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir
    main(input_dir, output_dir)
