def print_test_result(expected, got, tid):
    if got == expected:
        print(f'Test {tid} passed')
    else:
        print(f'Test {tid} failed\nExpected: {expected}\ngot: {got}')

def write(path: str, data: str):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(data)