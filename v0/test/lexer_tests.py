from os import remove

from src.tokens import *
from src.lexer import lexer
from .util import write, print_test_result

TEST_FILE_PATH = 'test.txt'

def get_repr(tokens: list[Token]) -> list[str]:
    return [t.__repr__() for t in tokens]

def get_tokens() -> list[str]:
    return get_repr(lexer(TEST_FILE_PATH))

def basic_parenthesis_test():
    write(TEST_FILE_PATH, '()\n()')
    tokens = get_tokens()
    expected = ['(', ')', ';', '(', ')', ';']
    print_test_result(expected, tokens, 1)

    write(TEST_FILE_PATH, '([\n])')
    tokens = get_tokens()
    expected = ['(', '[', ']', ')', ';']
    print_test_result(expected, tokens, 2)

    remove(TEST_FILE_PATH)

basic_parenthesis_test()