# functions of pre processing of the code.

# we need to add more stuff to this
class PreprocessError(SyntaxError):
    pass

# will compute every start and end indexes of strings so preprocessor can ignore them.
def computeStrings(code: str) -> list:
    isInString = False
    result: list = []
    startIndex: int = 0

    for i in range(len(code)):
        # is the given char a string opening / closing
        if code[i] == "\"" and i != 0 and code[i-1] != "\\":
            if isInString:
                result.append((startIndex, i + 1))
                isInString = False
            else:
                isInString = True
                startIndex = i

    return result

def removeComments(code: str) -> str:
    #strings: list = computeStrings(code)
    #stringCount = 0

    res: str = ""

    isInString = False

    # note to me: need to insert a \n to be at the end of the code.
    i = 0
    codeSize = len(code)
    lastCodeIndex = codeSize - 1

    while (i < codeSize):

        # check if is inside string
        if code[i] == '\"' and i != 0 and code[i-1] != '\\':
            isInString = not isInString

        # check for // comment
        if not isInString and i != lastCodeIndex and code[i] == '/' and code[i + 1] == '/':
            i = code.find("\n", i+1)
            # did not found end of file, which means it is the end of the code
            if (i == -1):
                break


        # check for /* comment
        if not isInString and i != lastCodeIndex and code[i] == '/' and code[i + 1] == '*':
            i = code.find("*/", i+1) + 2
            if (i == -1):
                # todo: add more description to here
                raise PreprocessError("No matching */ found for comment")

        res += code[i]
        i += 1

    return res
    
def trimUnnecessaryWhitespaces(code: str) -> str:
    res: str = ""
    isInString = False

    i = 0
    codeSize = len(code)

    while (i < codeSize):
        if code[i] == '\"' and i != 0 and code[i-1] != '\\':
            isInString = not isInString

        if not isInString and i > 0 and code[i].isspace() and res[-1] == code[i]:
            i += 1
            continue

        res += code[i]
        i += 1

    return res