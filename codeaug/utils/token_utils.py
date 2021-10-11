from pygments import highlight
from pygments.lexers import Python3Lexer
from pygments.formatters import HtmlFormatter, TerminalFormatter, TerminalTrueColorFormatter, Terminal256Formatter

import codeaug.utils.code_tokenizer as code_tokenizer

def peak(path: str, n=10) -> str:
    """reads first n lines from file"""
    with open(path, 'r') as f:
        head = list(islice(f, n)) 
    return "".join(head)

def detok(code, lang='python'):
    detokenize = getattr(code_tokenizer, f"detokenize_{lang}")
    return detokenize(code)

def tokenize(code, lang='python'):
    tokenize_ = getattr(code_tokenizer, f"tokenize_{lang}")
    return tokenize_(code)

def colored(code: str, formatter=Terminal256Formatter) -> str:
    return highlight(code, Python3Lexer(), formatter())

def remove_bpe(s: str):
    return s.replace(" ", "").replace("▁", " ").lstrip(' ')

