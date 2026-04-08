import sys
import subprocess
import os
import argparse

from tokens import *
from lexer import lexer


def run_compiler():
    parser = argparse.ArgumentParser(description="Mehadrin ל (Lamed) Transpiler")
    parser.add_argument("filename", help="The .ל source file to compile")
    parser.add_argument("-l", "--lazy", action="store_true", help="Use lazy space-separated POC translation")
    parser.add_argument("-k", "--keep", action="store_true", help="Keep the intermediate C source file")
    parser.add_argument("-o", "--output", dest="output_filename", help="The name of the output binary")
    
    args = parser.parse_args()

    if not os.path.exists(args.filename):
        print(f"Error: File '{args.filename}' not found.")
        sys.exit(1)

    tokens = lexer(args.filename)

    if args.lazy:
        # common headers, might need to add more
        c_code_parts = [
            "#include <stdio.h>",
            "#include <stdlib.h>",
            "#include <wchar.h>",
            "#include <locale.h>",
            "\n"
        ]

        translated_tokens = [t.to_c() for t in tokens]
        c_code_parts.append(" ".join(translated_tokens))

        c_source = "\n".join(c_code_parts)
    else:
        print("Standard parsing mode not implemented yet. Use -l for now.")
        sys.exit(1)

    temp_c_file = "lamed_temp_out.c"
    with open(temp_c_file, "w", encoding="utf-8") as f:
        f.write(c_source)

    # call gcc
    output_bin = args.output_filename if args.output_filename else "a.out"
    
    print(f"Compiling {args.filename} to {output_bin}...")
    
    gcc_cmd = ["gcc", temp_c_file, "-o", output_bin]
    
    try:
        result = subprocess.run(gcc_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print("Compilation Error from GCC:")
            print(result.stderr)
        else:
            print("Successfully compiled.")
    except FileNotFoundError:
        print("Error: GCC is not installed or not in PATH.")
    finally:
        if not args.keep:
            os.remove(temp_c_file)

if __name__ == "__main__":
    run_compiler()