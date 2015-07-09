#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main class that prints the python files of a directory and sub-directories
"""
import sys

from utils.path_walker import get_directory_structure


def main(base_path):
    """
    Iterates over found python files and prints file-path and file-name
    """
    for file_path, file_name in get_directory_structure(base_path):
        print(file_path, file_name)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(base_path=sys.argv[1])
    else:
        print("%s <directory to analyze>" % sys.argv[0])
