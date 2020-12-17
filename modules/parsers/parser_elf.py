#!/usr/bin/python3

from collections import OrderedDict
from pwnlib.elf import *
import logging

from modules.parsers.parser import Parser

class ParserElf(Parser):
    filetype_regex = 'ELF.*'

    def __init__(self, filename, output_filename):
        super(ParserElf, self).__init__(filename, output_filename)
        try:
            self.file = ELF(self.filename)
        except FileNotFoundError:
            logging.error("Could not find provided file under current location: {}".format(self.filename))
            exit(1)
        except Exception as e:
            logging.error("File is not a proper ELF file! Exiting...".format(self.filename))
            exit(1)

        self.symbolsOrdered = OrderedDict({k: v for k, v in sorted(self.file.symbols.items(), key=lambda item: item[1])})

    def disassemble(self):
        string = ''
        for fname, function in self.file.functions.items():
            if string:
                string += '\n'
            string += "{}:\n".format(fname)
            string += self.file.disasm(function.address, int(str(function.size), 16))
        return string


    def edit(self, hexdump, address, newBytes):
        #returns edited COPY of provided hexdump
        edited = hexdump.copy()
        address = int(address, 16)
        iter = 0
        for newByte in newBytes:
            try:
                edited[hex(address+iter)] = newByte
                logging.debug("Changing {} byte to {}".format(hex(address+iter), newByte))
                iter += 1
            except KeyError:
                logging.error("Could not find address: {}".format(hex(address+iter)))
                exit(1)
        return edited

#legacy approach from before switching to free pwn lib. It was so beautifull I couldn't remove it ;_(
    def hexdump(self):
        #creates similar hexdump as linux hexdump command but with virtual addressation and byte by byte entries
        hexdump = OrderedDict()
        offset = self.file.address
        with open(self.filename, "r+b") as f:
            address = self.file.address
            for byte in iter(lambda: f.read(1), b''):
                adress_str = self.convertAdressToHex(address)
                byte_str = hex(int.from_bytes(byte, 'big'))[2:]
                hexdump[adress_str] = byte_str
                address += 1
        return hexdump

#legacy approach from before switching to free pwn lib. It was so beautifull I couldn't remove it ;_(
    def printableHexdump(self, hexdump):
        #prints similar hexdump as linux hexdump command but with virtual addressation
        printable_hexdump = OrderedDict()
        i = 0
        adresses = ""
        chars = ""
        for address, hexVar in hexdump.items():
            if i == 0:
                adress_str = "{}".format(address)
            adresses = "{}{} ".format(adresses, hexVar.ljust(2))
            try:
                #ignore nonprintable ASCII characters
                if int(hexVar, 16) < 20:
                    chars = "{}{}".format(chars, '.')
                else:
                    chars = "{}{}".format(chars, bytes.fromhex(hexVar.zfill(2)).decode("ASCII"))
            except UnicodeDecodeError:
                chars = "{}{}".format(chars, '.')
            if i == 7:
                adresses += " "
            if i == 15:
                printable_hexdump[adress_str] = "{} |{}|".format(adresses, chars)
                i = 0
                adresses = ""
                chars = ""
            else:
                i += 1
        string = ''
        for address, line in printable_hexdump.items():
            if string:
                string += '\n'
            string += "{}: {}".format(address, line)
        logging.debug("Printable hexdump generated.")
        return string