import os
from interface import *
from . import Instruction

"""
Scans the Pseudo Code Language file set based on settings
"""


class File:
    file = filename = None
    instructions = []

    @classmethod
    def run(cls):
        """
        Specifies which methods to run
        """
        cls.setFilename()
        cls.readFile()
        Display.separateSections()

    @classmethod
    def setFilename(cls):
        """
        Sets the file name and path according to the settings
        """
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        if Settings.getProgram() == 1:
            cls.filename = "prog_1.txt"
            filePath = os.path.join(fileDir, "programs\\" + cls.filename)
            cls.file = os.path.abspath(os.path.realpath(filePath))

        elif Settings.getProgram() == 2:
            cls.filename = "prog_2.txt"
            filePath = os.path.join(fileDir, "programs\\" + cls.filename)
            cls.file = os.path.abspath(os.path.realpath(filePath))

    @classmethod
    def readFile(cls):
        """
        Remove spaces and linebreaks and strips lines to the first 11 characters (10 numbers and sign)
        Display error if file contains a non-confirm opCode
        """
        with open(cls.file, "r") as lines:
            for line in lines:
                if not line.startswith("#") and not line.startswith("\n"):
                    line = line.partition("#")[0].rstrip()
                    instruction = Instruction(line)
                    cls.instructions.append(instruction)
                    if not cls.syntaxCheck(instruction):
                        print(Fore.CYAN + "Syntax Check:")
                        print("-------------" + Fore.RESET)
                        print(Fore.RED + "\n(!) Undefined syntax in line " +
                              repr(len(cls.instructions)) + " '" +
                              instruction.stream + "' in file " + "'" + cls.filename + "'" + Fore.RESET)
                        cls.instructions = []
                        break
            if len(cls.instructions) != 0:
                print(Fore.CYAN + "Syntax Check:")
                print("-------------" + Fore.RESET)
                print(Fore.GREEN + "\n(+) Valid syntax in file " + "'" + cls.filename + "'" + Fore.RESET)

    @classmethod
    def syntaxCheck(cls, instruction):
        """
        Checks if opCode is correct
        :param instruction: instruction to be checked
        :return: True if valid opCode, False otherwise
        """
        return instruction.isValid()
