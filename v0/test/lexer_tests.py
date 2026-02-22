from os import remove

from src.tokens import *
from src.lexer import lexer
from .util import write, print_test_result, print_test_suite_title

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

    write(TEST_FILE_PATH, "== != <= >= && || ->")
    tokens = get_tokens()
    expected = ['==', '!=', '<=', '>=', '&&', '||', '->', ';']
    print_test_result(expected, tokens, 8)

def basic_number_test():
    write(TEST_FILE_PATH, "123 0.456 .789")
    tokens = get_tokens()
    expected = ['Int(123)', 'Float(0.456)', 'Float(0.789)', ';']
    print_test_result(expected, tokens, 9)

    write(TEST_FILE_PATH, "42. 007")
    tokens = get_tokens()
    expected = ['Float(42.0)', 'Int(7)', ';']
    print_test_result(expected, tokens, 10)

def basic_identifier_keyword_test():
    write(TEST_FILE_PATH, "שלם x = 10")
    tokens = get_tokens()
    expected = ['int', 'Identifier(x)', '=', 'Int(10)', ';']
    print_test_result(expected, tokens, 11)

    write(TEST_FILE_PATH, "החזר מספר_123")
    tokens = get_tokens()
    expected = ['return', 'Identifier(מספר_123)', ';']
    print_test_result(expected, tokens, 12)

def complex_combination_test():
    write(TEST_FILE_PATH, "אם(מספר==10){החזר 0}")
    tokens = get_tokens()
    expected = [
        'if', '(', 'Identifier(מספר)', '==', 'Int(10)', ')', 
        '{', 'return', 'Int(0)', ';', '}', ';'
    ]
    print_test_result(expected, tokens, 13)

print_test_suite_title("Lexer Tests")
basic_parenthesis_test()
basic_string_char_test()
basic_operator_test()
basic_number_test()
basic_identifier_keyword_test()
complex_combination_test()

remove(TEST_FILE_PATH)