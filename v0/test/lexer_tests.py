from os import remove

from src.tokens import *
from src.lexer import lexer
from .util import write, print_test_result

TEST_FILE_PATH = 'test.txt'

def get_repr(tokens: list[Token]) -> list[str]:
    return [str(t) for t in tokens]

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

def basic_string_char_test():
    write(TEST_FILE_PATH, '"שלום, עולם!"')
    tokens = get_tokens()
    expected = ['String("שלום, עולם!")', ';']
    print_test_result(expected, tokens, 3)

    write(TEST_FILE_PATH, "'א'")
    tokens = get_tokens()
    expected = ['Char(\'א\')', ';']
    print_test_result(expected, tokens, 4)

    write(TEST_FILE_PATH, "'\\ט'")
    tokens = get_tokens()
    expected = ["Char('\t')", ';']
    print_test_result(expected, tokens, 5)

    write(TEST_FILE_PATH, '"מחרוזת" "מחרוזת"')
    tokens = get_tokens()
    expected = ['String("מחרוזת")', 'String("מחרוזת")', ';']
    print_test_result(expected, tokens, 6)

def basic_operator_test():
    write(TEST_FILE_PATH, "+-*%")
    tokens = get_tokens()
    expected = ['+', '-', '*', '%', ';']
    print_test_result(expected, tokens, 7)

basic_parenthesis_test()
basic_string_char_test()
basic_operator_test()

remove(TEST_FILE_PATH)