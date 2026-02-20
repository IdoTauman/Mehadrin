# used to get the file from CLI arguments.
import sys
import os

if (len(sys.argv) != 2):
    print("unknown arguments.")

path = sys.argv[1]

if not os.path.isfile(path):
    print(f"file {path} not found.")

with open(path, "r") as file:
    content: str = file.read()
    splitted = content.split("\n")