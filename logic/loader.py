from interface import *
from . import File
from . import Parser
from . import Instruction
import time

"""
    Initializes memory with data and program
"""


class Loader:
    data = [None] * 1000  # Data array initialized at None x 1000
    program = [None] * 1000  # Program array initialized at None x 1000
    input = []  # Input array to be filled later

    @classmethod
    def run(cls):
        """
        Specifies which methods to run
        """
        cls.load()
        cls.setInput()

    @classmethod
    def load(cls):
        """
        Goes through the instructions and sets blocks divided by +9 999 999 999
        Each sections is saved into the corresponding memory location
        Special operations occur for input depending on settings
        """
        block = index = 0
        if Parser.needsParsing:
            instructions = Parser.instructions
        else:
            instructions = File.instructions
        for instruction in instructions:
            instruction = instruction.stream.replace(" ", "")

            if instruction != "+9999999999":
                if block == 0:
                    cls.data[index] = int(instruction)
                    index += 1
                if block == 1:
                    cls.program[index] = instruction
                    index += 1
                if block == 2:
                    cls.input = [None] * int(instruction)  # Initialize input array with set size
            else:
                block += 1  # Move to next block
                index = 0  # Reset index to 0

    @classmethod
    def getDataIndex(cls):
        return next(i for i in Loader.data if i is None)

    @classmethod
    def isDataFull(cls):
        return None not in cls.data

    @classmethod
    def setInput(cls):
        """
        Fills input array either with manual input or with values from assignment
        """
        # if Settings.getInputMethod() == "Manual":
        #     index = 0
        #     for i in range(0, len(cls.input)):
        #         while True:
        #             try:
        #                 print(Fore.RESET + "Enter the value #" + repr(index + 1) + ":\t" + Fore.CYAN, end='')
        #                 cls.input[index] = int(input())
        #                 index += 1
        #             except ValueError:
        #                 print(Fore.RED + "Invalid value" + Fore.RESET)
        #             else:
        #                 break
        #     Display.separateSections()
        if Settings.getInputMethod() == "Automatic":
            values = [1125, -761, 0, -5468, -204, 1987658, -1234567891, 205, -34657899, -355]
            for index, value in enumerate(values):
                cls.input[index] = int(value)

    @classmethod
    def displayMemory(cls):
        if Settings.getInputMethod() == "Automatic":
            cls.displayInput()
            Display.separateSections()
            # time.sleep(1.5)
        cls.displayData()
        Display.separateSections()
        # time.sleep(1.5)
        cls.displayProgram()
        Display.separateSections()

    @classmethod
    def displayData(cls):
        if Settings.done is False:
            print(Fore.CYAN + "Initial Data:")
            print("-------------\n" + Fore.RESET)
        else:
            print(Fore.CYAN + "Final Data:")
            print("-----------\n" + Fore.RESET)

        data = [["Address", "Value"]]
        for index, value in enumerate(cls.data):
            if value is not None:
                data.append([index, "{:,}".format(value)])

        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.set_cols_dtype(['i', 'i'])
        table.set_cols_align(["r", "r"])
        table.add_rows(data)
        print(table.draw())

    @classmethod
    def displayProgram(cls):
        print(Fore.CYAN + "Program:")
        print("--------\n" + Fore.RESET)

        if Parser.needsParsing:
            program = [
                ["Line", "Assembly like Instruction", "Numeric Instruction", "Operator", "Operand 1", "Operand 2",
                 "Operand 3"]
            ]
            iterator = 0
            for index, value in enumerate(cls.program):
                if value is not None:
                    instruction = Instruction(value[0:2] + " " + cls.whiteSpace(value[2:11], 3))
                    program.append(
                        [index,
                         Parser.program[iterator].stream,
                         instruction.stream,
                         instruction.operator + " : " + list(Instruction.operators.keys())[list(Instruction.operators.values()).index(instruction.operator)],
                         instruction.operand_1, instruction.operand_2,
                         instruction.operand_3])
                iterator += 1
            table = Texttable()
            table.set_deco(Texttable.HEADER)
            table.set_cols_width([10, 25, 25, 10, 10, 10 ,10])
            table.set_cols_dtype(['i', 't', 't', 't', 't', 't', 't'])
            table.set_cols_align(["r", "l", "l", "r", "r", "r", "r"])
            table.add_rows(program)
            print(table.draw())
        else:
            program = [
                ["Line", "Instruction", "Operator", "Operand 1", "Operand 2", "Operand 3"]]
            for index, value in enumerate(cls.program):
                if value is not None:
                    instruction = Instruction(value[0:2] + " " + cls.whiteSpace(value[2:11], 3))
                    program.append(
                        [index, instruction.stream,
                         instruction.operator + " : " + list(Instruction.operators.keys())[list(Instruction.operators.values()).index(instruction.operator)],
                         instruction.operand_1, instruction.operand_2,
                         instruction.operand_3])

            table = Texttable()
            table.set_deco(Texttable.HEADER)
            table.set_cols_dtype(['i', 't', 't', 't', 't', 't'])
            table.set_cols_align(["r", "r", "r", "r", "r", "r"])
            table.add_rows(program)
            print(table.draw())

    @classmethod
    def displayInput(cls):
        print(Fore.CYAN + "Automatic Input:")
        print("----------------\n" + Fore.RESET)

        input = [["#", "Value"]]
        for index, value in enumerate(cls.input):
            if value is not None:
                input.append([index + 1, "{:,}".format(value)])

        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.set_cols_dtype(['i', 'i'])
        table.set_cols_align(["r", "r"])
        table.add_rows(input)
        print(table.draw())

    @staticmethod
    def whiteSpace(string, length):
        """
        Adds whitespace every "length" characters
        :param string:
        :param length:
        :return:
        """
        return ' '.join(string[i:i + length] for i in range(0, len(string), length))
