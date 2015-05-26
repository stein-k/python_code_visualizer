#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from .path_walker import get_directory_structure


def main(base_path):
    for file_path, file_name in get_directory_structure(base_path):
        print(file_path, file_name)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("%s <directory to analyze>" % sys.argv[0])
