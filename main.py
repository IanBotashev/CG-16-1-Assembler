#!/usr/bin/env python3
from tokenizer.tokenizer import Tokenizer
import argparse


def main(command_args):
    tokenizer = Tokenizer(hex_indicator=command_args.hex_indicator,
                          binary_indicator=command_args.binary_indicator,
                          address_indicator=command_args.address_indicator,
                          allow_overflow=command_args.allow_overflow)
    tokens = tokenizer.parse_file(command_args.file_path)
    print(tokens)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="BAssembler", description="Basic and naive assembler for the CG-16-1 processor.")
    parser.add_argument("--hex_indicator", '-hi', default="0x",
                        help="Sets what character(s) indicate a hexadecimal when put at the beginning of a number.")
    parser.add_argument("--binary_indicator", "-bi", default="0b",
                        help="Sets what character(s) indicate binary when put at the beginning of a number.")
    parser.add_argument("--address_indicator", "-ai", default="$",
                        help="Sets what character(s) indicate an address when put at the beginning of a number.")
    parser.add_argument("--allow_overflow", "-of", action="store_true",
                        help="If set, assembler won't throw error if a value is higher than the 16-bit int limit.")
    parser.add_argument("file_path", help="File to compile to binary")

    args = parser.parse_args()
    try:
        main(args)
    except KeyboardInterrupt:
        print("Goodbye...")
        exit()
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
