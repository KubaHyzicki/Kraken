#!/usr/bin/env python3

import argparse
import logging

from modules.krakenUI import KrakenUI

def hexdump(kraken, args):
    kraken.printHexdump()

def disassemble(kraken, args):
    kraken.disassemble()

def edit(kraken, args):
    kraken.edit(args.address, args.bytes)

def parse_arguments():
    parser = argparse.ArgumentParser()

    #base args
    parser.add_argument('file', help = 'Binary file to parse')
    parser.add_argument('--format', '-f', required = False, choices = ['elf'], help = 'Format of a binary e.g. elf')
    parser.add_argument('--verbose', '-v', action = 'store_true', required = False, help = 'Sets logging type to DEBUG')

    subparser = parser.add_subparsers(
        title = 'mode',
        dest = 'mode'
    )
    subparser.required = True

    #hexdump mode
    parser_hexdump = subparser.add_parser('hexdump', help = 'Parses file and prints its hexdump')
    parser_hexdump.set_defaults(mode = hexdump)
    parser_hexdump.add_argument('--output', '-o', required = False, help = 'Output will be saved as file with provided filename')

    #disassemble mode
    parser_disassemble = subparser.add_parser('disassemble', help = 'Parses file and disassembles it')
    parser_disassemble.set_defaults(mode = disassemble)
    parser_disassemble.add_argument('--output', '-o', required = False, help = 'Output will be saved as file with provided filename')

    #edit mode
    parser_edit = subparser.add_parser('edit', help = 'Changes data of a binary')
    parser_edit.set_defaults(mode = edit)
    parser_edit.add_argument('--address', '-a', required = False, help = 'Addres from which new bytes will be written')
    parser_edit.add_argument('--bytes', '-b', nargs = '+', type = str, required = True, metavar = 'BYTE', help = 'Bytes set to be written')
    parser_edit.add_argument('--output', '-o', required = True, help = 'Output will be saved as file with provided filename')


    return parser.parse_args()

def main():
    args = parse_arguments()

    if args.format:
        kraken = KrakenUI(args.file, args.output, args.format)
    else:
        kraken = KrakenUI(args.file, args.output)

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        kraken.verbose = True
    else:
        logging.getLogger().setLevel(logging.INFO)

    args.mode(kraken, args)

if __name__ == "__main__":
    main()
