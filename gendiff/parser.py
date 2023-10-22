import argparse


from gendiff import stylish
from gendiff import plain
from gendiff import json


def create_parser() -> object:
    """
    Parser arguments
    """
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.'
    )
    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)
    parser.add_argument(
        '-f', '--format',
        help='set format of output'
    )

    dict_style = {
        'plain': plain,
        'json': json,
        'stylish': stylish
    }

    args = parser.parse_args()
    args.format = dict_style[args.format] \
        if args.format \
        else dict_style['stylish']

    return args