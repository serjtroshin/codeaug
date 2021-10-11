## Features
- 11.10.21: Variable Misuse:
```
>>> from codeaug import VarMisuse
>>> code_example ="""
    my_file = "input.txt"
    with open(my_file, "r") as f:
        print(f.readlines())
    """
>>> varmisuse = VarMisuse("python")
>>> print(varmisuse(code_example, p=1.0))

    print = "input.txt"
    with my_file(readlines, "r") as print:
        readlines(print.print())
```

## 1. Installation
- Run installation script:
```
git clone https://github.com/serjtroshin/codeaug
cd codeaug
pip install -e .
```