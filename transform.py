import argparse
from codeaug.varm import VarMisuse
from codeaug.utils.token_utils import tokenize, detok

import os

def add_varmisuse(tokens, lang, args):
    varmisuse = VarMisuse(lang, args.tree_sitter_path, p=1)
    return tokenize(varmisuse(detok(tokens)))

if __name__=="__main__":
    parser = argparse.ArgumentParser("varmisuse")
    parser.add_argument("--tree_sitter_path", default="~/PLBART/evaluation/CodeBLEU/parser/my-languages.so")
    args = parser.parse_args()
    args.tree_sitter_path = os.path.expanduser(args.tree_sitter_path)
    input = ["def", "get", "(", ")", ":", 'NEW_LINE', "INDENT", "a", "=", "b", 'NEW_LINE', "DEDENT"]
    print(input)
    print(add_varmisuse(input, "python", args))