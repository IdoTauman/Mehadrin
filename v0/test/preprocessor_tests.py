import src.preprocessor as PreP

def printBarrier(name = ""):
    if name != "":
        print(f"\n\n------------------------ {name} ------------------------- \n\n")
        return
    print("\n\n------------------------------------------------------------- \n\n")

import sys
import os

if (len(sys.argv) != 2):
    print("unknown arguments.")

path = sys.argv[1]

if not os.path.isfile(path):
    print(f"file {path} not found.")

with open(path, "r") as file:
    content: str = file.read()

    printBarrier("given file")

    print(content)

    printBarrier("remove comment")


    #splitted = content.split("\n")
    #strings = PreP.computeStrings(content)
    #for tup in strings:
    #    print(content[tup[0]:tup[1]])

    #printBarrier()


    print(PreP.removeComments(content))

printBarrier()

