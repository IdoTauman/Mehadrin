def print_test_result(expected, got, tid):
    if got == expected:
        print(f'Test {tid} passed')
    else:
        print(f'Test {tid} failed\nExpected: {expected}\ngot: {got}')

def print_test_suite_title(title):
    print('\n' + '-' * 10 + title + '-' * 10)

def write(path: str, data: str):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(data)