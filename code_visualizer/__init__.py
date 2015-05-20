#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from pprint import pprint

from code_visualizer.ast_parser.code_parser import CodeParser


def get_directory_structure(path):
    structure = {}
    for root, directories, filenames in os.walk(path):
        if ".git" in directories:
            directories.remove(".git")
        if ".svn" in directories:
            directories.remove(".svn")
        structure[root] = filenames
    return structure


def main(base_path):
    if os.path.isdir(base_path):
        directory_structure = get_directory_structure(base_path)
        ast_code_parser = CodeParser()

        counters = {}
        for directory, file_names in directory_structure.items():
            for file_name in file_names:
                if file_name.endswith(".py"):
                    path_to_python_file = os.path.join(directory, file_name)
                    with open(path_to_python_file) as python_file:
                        python_code_as_string = python_file.read()
                        parsed_map = ast_code_parser.parse_python_code(python_code_as_string)
                        nodes = parsed_map.get('', ).get('children')

                        # filter on imports only
                        #nodes = {key: value for key, value in nodes.items() if 'import' == value.get('type')}

                        counters[path_to_python_file] = nodes

        pprint(counters)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("%s <directory to analyze>" % sys.argv[0])
