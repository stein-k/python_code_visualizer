#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from pprint import pprint

from simple_counter import code_counter


def get_directory_structure(path):
    structure = {}
    for root, directories, filenames in os.walk(path):
        if ".git" in directories:
            directories.remove(".git")
        if ".svn" in directories:
            directories.remove(".svn")
        structure[root] = filenames
    return structure


def main(path):
    if os.path.isdir(path):
        directory_structure = get_directory_structure(path)

        counters = {}
        for directory, filenames in directory_structure.items():
            for filename in filenames:
                if filename.endswith(".py"):
                    path_to_python_file = os.path.join(directory, filename)
                    with open(path_to_python_file) as python_file:
                        python_code_as_string = python_file.read()
                        counters[path_to_python_file] = code_counter.get_counters_for_file(python_code_as_string)

        pprint(counters)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("%s <directory to analyze>")
