from functools import reduce
from gendiff.cli.open_check_file import open_check_file
from gendiff.formatters.stylish import stylish
from gendiff.formatters.plain import plain
from gendiff.formatters.json import json


def is_not_none(dict_: dict, key: str) -> bool:
    """
    key in dict
    """
    return dict_.get(key) is not None


def format_bool_value(key, node):
    """
    Lower case for bool value
    """
    value = node[key]
    if value is None:
        return str('null')

    if key in node:
        return str(value).lower() \
            if value is True or value is False \
            else value


def generate_diff(
    dict1: dict,
    dict2: dict,
    format_name='stylish'
) -> dict:
    """
    Calculates the difference between files
    result - > dict
    {
    key: ['flag_action', *value]
    }

    flag_action:
    add, unchange, change, del
    """

    styles = {
        'plain': plain,
        'json': json,
        'stylish': stylish
    }

    formatter = styles[format_name]

    # was realise in individual modul
    # but for test need realise here
    dict1, dict2 = open_check_file(dict1, dict2) \
        if isinstance(dict1, str) and isinstance(dict2, str) \
        else (dict1, dict2)

    def inner(node1, node2):

        intersection_keys = node1.keys() & node2.keys()
        sort_all_keys = sorted(node1.keys() | node2.keys())

        def searcher(key):
            """
            Function searcher, for concate result
            """
            key_in_dict1 = is_not_none(node1, key)

            if key in intersection_keys:

                value1 = format_bool_value(key, node1)
                value2 = format_bool_value(key, node2)

                if value1 == value2:
                    return {key: ['unchange', value1]}

                # if values is dict -> recursion
                if (
                    isinstance(
                        value1, dict
                    ) and isinstance(
                        value2, dict
                    )
                ):
                    return {key: inner(value1, value2)}

                else:
                    return {
                        key: ['change', value1, value2]
                    }

            else:
                return {key: ['del', format_bool_value(key, node1)]} \
                    if key_in_dict1 \
                    else {key: ['add', format_bool_value(key, node2)]}

        result = reduce(lambda x, y: x | y, map(searcher, sort_all_keys), {})
        return result

    return formatter(inner(dict1, dict2))