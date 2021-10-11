import os
import argparse

from codeaug.varm import VarMisuse

code_example ="""
    my_file = "input.txt"
    with open(my_file, "r") as f:
        print(f.readlines())
    """
varmisuse = VarMisuse("python", p=1.0)
print(code_example)
print(varmisuse(code_example))

