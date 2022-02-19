import os
import argparse
from pathlib import Path

from codeaug.utils.token_utils import detok, colored, tokenize
from codeaug.utils.tree_utils import TreeSitterCode, traverse_tree
from codeaug.utils.fast_dict import ListDict

from tree_sitter import Language, Parser, Tree, Node

import random
from random import randint
from copy import deepcopy
import numpy as np

random.seed(1)
np.random.seed(1)

DIR = os.path.abspath(Path(__file__, "..", ".."))
tree_sitter_path=str(Path(DIR, "parser", "my-languages.so"))


def insert_variable_misuse(code_tree: TreeSitterCode, p=0.1, crop=3) -> str:
    # returns status. if False: skip
    values = list(code_tree.identifiers())
    unique_values = ListDict()
    for value in values:
        unique_values.add(code_tree.get_value(value))
    if len(unique_values) < crop:
        return None
    
    start_byte = 0
    code_fragments = [] # except values
    where_is_value = {}
    for idx, value in enumerate(values):
        end_byte = value.start_byte
        code_fragments.append(code_tree.code_bytes[start_byte:end_byte])
        where_is_value[idx] = len(code_fragments)
        code_fragments.append(code_tree.get_value(value))
        start_byte = value.end_byte
        
    code_fragments.append(code_tree.code_bytes[start_byte:])
    values = [code_tree.get_value(value) for value in values] # Node -> str
    
    # for each variable name choose if it is replaced
    is_replaced = np.random.uniform(size=len(values)) < p
    replaced_idxs = np.arange(len(values))[is_replaced]
    
    for idx, value in enumerate(values):
        if not is_replaced[idx]:
            continue
        unique_values.remove(value)
        other = unique_values.choice() # choice over default set is slow
        unique_values.add(value)
        # print(code_fragments[where_is_value[idx]], "-->", other)
        code_fragments[where_is_value[idx]] = other # insert a "varmisuse bug"
    final_code = b"".join(code_fragments)
    return final_code.decode()

class VarMisuse:
    def __init__(self, lang: str):
        
        assert lang in ["python", "java"]
        LANGUAGE = Language(tree_sitter_path, lang)
        parser = Parser()
        parser.set_language(LANGUAGE)
        self.parser = parser
    
    def __call__(self, code_example, p=0.0):
        code = TreeSitterCode(code_example, self.parser)
        # print(colored(code.code))
        bugged_code = insert_variable_misuse(code, p=p)
        # print(colored(bugged_code))
        return bugged_code


def add_varmisuse_args(parser):
    parser.add_argument("--tree_sitter_path", default="parser/my-languages.so")


if __name__=="__main__":
    parser = argparse.ArgumentParser("varmisuse")
    add_varmisuse_args(parser)
    args = parser.parse_args()
    args.tree_sitter_path = os.path.expanduser(args.tree_sitter_path)

    PY_LANGUAGE = Language(args.tree_sitter_path, 'python')
    JAVA_LANGUAGE = Language(args.tree_sitter_path, 'java')


    code_example ="""
    my_file = "input.txt"
    with open(my_file, "r") as f:
        print(f.readlines())
    """

    parser = Parser()
    parser.set_language(PY_LANGUAGE)
    code = TreeSitterCode(code_example, parser)

    print("<With no bug>")
    print(colored(code.code))

    seed = 1
    random.seed(seed)
    np.random.seed(seed)
    bugged_code = insert_variable_misuse(code, p=0.2)
    print()
    print(f"<With a bug >")
    print(colored(bugged_code))


    varmisuse = VarMisuse("python", args.tree_sitter_path)
    print(colored(varmisuse(code_example)))