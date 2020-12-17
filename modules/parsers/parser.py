#!/usr/bin/python3

import logging
import magic
import re

class Parser:
    filetype_regex = '.*'
    def __init__(self, filename, output_filename):
        self.filename = filename
        self.output_filename = output_filename
        if not self.checkFormat():
            logging.error("Provided file is in incorrect format! Exiting")
            exit(1)

    def hexdump(self):
        raise NotImplementedError()

    def printableHexdump(self):
        raise NotImplementedError()

    def disassemble(self):
        raise NotImplementedError()

    def edit(self, hexdump, address, newBytes):
        raise NotImplementedError()

    def checkFormat(self):
        filetype = magic.from_file(self.filename)
        if re.match(self.filetype_regex, filetype):
            return True
        else:
            logging.warning("Checked file format is {}".format(filetype))
            return False

    def convertAdressToHex(self, int_val, length = 7):
        hex_val = hex(int_val)
        hex_val = hex_val[2:]
        while len(hex_val) < length:
            hex_val = "0" + hex_val
        return '0x' + hex_val

    def compare_hexdumps(self, hexdump_1, hexdump_2):
        diff = "Changes made"
        for key, value in hexdump_1.items():
            if value == hexdump_2[key]:
                continue
            diff += "\n{}:\n- {}\n+ {}".format(key, value, hexdump_2[key])
        if len(diff) == 7:
            logging.warning("No changes made!")
        else:
            logging.debug("Diff generated")
            print(diff)

    def saveBinaryFile(self, hexdump):
        if not self.output_filename:
            logging.error("No output file provided!")
        byteArray = bytearray()
        for adress, byte in hexdump.items():
            byteArray.append(int(byte, 16))
        with open(self.output_filename, 'w+b') as f:
            f.write(byteArray)
        logging.info("Binary successfully saved as {}".format(self.output_filename))

    def saveTextFile(self, hexdump):
        if not self.output_filename:
            logging.error("No output file provided!")
        with open(self.output_filename, 'w') as f:
            f.write(hexdump)
        logging.info("Output successfully saved as {}".format(self.output_filename))

    def validateBytes(self, checked_bytes):
        validated = True
        for byte in checked_bytes:
            try:
                byteInt = int(byte, 16)
                if byteInt < 0 or byteInt > 127:
                    raise ValueError("Byte out of ASCII range")
            except Exception as e:
                validated = False
                print(e)
                logging.warning("Byte '{}' is not correct!".format(byte))
        return validated

    def validateAddress(self, checked_address):
        validated = True
        try:
            address = int(checked_address, 16)
        except Exception as e:
            validated = False
            print(e)
            logging.warning("Address '{}' is not correct!".format(checked_address))
        return validated
