import argparse
from pprint import pprint

from python_code_visualizer.recipes.file_paths_and_code_properties import as_dict

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='List dependencies and structure of python code')

    parser.add_argument('input_dir', help='The base path for the code to visualize.')

    args = parser.parse_args()

    input_dir = args.input_dir
    output = as_dict(input_dir)
    pprint(output)