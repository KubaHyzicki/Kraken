#!/usr/bin/env python3

import logging

from modules.parsers.parser import Parser
from modules.parsers.parser_elf import ParserElf

logging.basicConfig(level = "INFO")

class KrakenUI:
    def __init__(self, file, output_file = None, format = 'elf'):
        self.filename = file
        self.format = format
        self.output_file = output_file

        self.verbose = False

        if format == 'elf':
            self.parser = ParserElf(self.filename, self.output_file)

    def printHexdump(self):
        hexdump = self.parser.hexdump()
        string = self.parser.printableHexdump(hexdump)
        if self.output_file:
            self.parser.saveTextFile(string)
            if self.verbose:
                print(string)
        else:
            print(string)

    def disassemble(self):
        string = self.parser.disassemble()
        if self.output_file:
            self.parser.saveTextFile(string)
            if self.verbose:
                print(string)
        else:
            print(string)


    def edit(self, address, newBytes):
        if not self.parser.validateBytes(newBytes):
            logging.error("Some of the provided bytes are incorrect! Exiting...")
            exit(1)
        if not self.parser.validateAddress(address):
            logging.error("Provided address is incorrect! Exiting...")
            exit(1)
        hexdump = self.parser.hexdump()
        edited_hexdump = self.parser.edit(hexdump, address, newBytes)
        if self.verbose:
            self.parser.compare_hexdumps(hexdump, edited_hexdump)
        self.parser.saveBinaryFile(edited_hexdump)  
