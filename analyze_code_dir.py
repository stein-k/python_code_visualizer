import argparse
from pprint import pprint

from python_code_visualizer.__main__ import main

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Visualize dependencies and structure of python code')

    parser.add_argument('input_dir', help='The base path for the code to visualize.')

    args = parser.parse_args()

    input_dir = args.input_dir
    output = main(input_dir)
    pprint(output)