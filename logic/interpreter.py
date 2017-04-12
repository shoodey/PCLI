from logic import *
from interface import *
import math, time

"""
    Interprets the program that is loaded into memory
"""


class Interpreter:
    errors = []
    indexToRead = 0

    @classmethod
    def run(cls):
        """
        Specifies which methods to run
        """
        cls.valueToRead = len(Loader.input)
        print(Fore.CYAN + "Runtime simulator (delay for dramatization purposes)")
        print("----------------------------------------------------\n" + Fore.RESET)
        print("#\tLine\t\tOperator\tOp1\t\tOp2\t\tOp3")
        print("=====\t========\t========\t===\t\t===\t\t===")
        cls.process()

    @classmethod
    def process(cls):

        index = counter = 0
        code_lines = Loader.program
        line_number = len([line for line in code_lines if line is not None])

        while index < line_number:
            line = code_lines[index]
            if line is not None and len(cls.errors) == 0:  # Line is an instruction and no errors so far
                instruction = Instruction(line[0:2] + " " + cls.whiteSpace(line[2:11], 3))

                cls.debug(instruction, index, counter)
                counter += 1

                if instruction.operator == "+0":
                    cls.assign(instruction, index)
                elif instruction.operator == "+1":
                    cls.add(instruction, index)
                elif instruction.operator == "-1":
                    cls.subtract(instruction, index)
                elif instruction.operator == "+2":
                    cls.multiply(instruction, index)
                elif instruction.operator == "-2":
                    cls.divide(instruction, index)
                elif instruction.operator == "+3":
                    cls.power(instruction, index)
                elif instruction.operator == "-3":
                    cls.root(instruction, index)
                elif instruction.operator == "+4":
                    index = cls.isEqual(instruction, index)
                    continue
                elif instruction.operator == "-4":
                    index = cls.isDifferent(instruction, index)
                    continue
                elif instruction.operator == "+5":
                    index = cls.isGreaterOrEqual(instruction, index)
                    continue
                elif instruction.operator == "-5":
                    index = cls.isLess(instruction, index)
                    continue
                elif instruction.operator == "+6":
                    cls.get(instruction, index)
                elif instruction.operator == "-6":
                    cls.put(instruction, index)
                elif instruction.operator == "+7":
                    index = cls.loop(instruction, index)
                    continue
                elif instruction.operator == "+8":
                    cls.read(instruction, index)
                elif instruction.operator == "-8":
                    cls.print(instruction, index)
                elif instruction.operator == "+9":
                    cls.stop()
            index += 1

    @classmethod
    def debug(cls, instruction, index, counter):
        if Parser.needsParsing:
            if instruction.operator != "+5" and instruction.operator != "-5" and instruction.operator != "+7":
                print(Fore.RESET + "(#" + repr(counter) + ")\t(Line " + repr(
                    index) + ")\t" +
                      instruction.operator + " : " + list(Instruction.operators.keys())[
                          list(Instruction.operators.values()).index(instruction.operator)] +
                      "\t" + cls.getVariableName(instruction.operand_1) + "\t\t" + cls.getVariableName(
                    instruction.operand_2) + "\t\t" + cls.getVariableName(instruction.operand_3))
            else:
                print(Fore.RESET + "(#" + repr(counter) + ")\t(Line " + repr(
                    index) + ")\t" +
                      instruction.operator + " : " + list(Instruction.operators.keys())[
                          list(Instruction.operators.values()).index(instruction.operator)] +
                      "\t" + cls.getVariableName(instruction.operand_1) + "\t\t" + cls.getVariableName(
                    instruction.operand_2) + "\t\t" + cls.getLabelName(instruction.operand_3))
        else:
            print(Fore.RESET + "(#" + repr(counter) + ")\t(Line " + repr(
                index) + ")\t" +
                  instruction.operator + " : " + list(Instruction.operators.keys())[
                      list(Instruction.operators.values()).index(instruction.operator)] +
                  "\t" + instruction.operand_1 + "\t\t" + instruction.operand_2 + "\t\t" + instruction.operand_3)
            # time.sleep(0.1)

    @classmethod
    def setError(cls, index, message="Result exceeds limit size (10)"):
        cls.errors.append("Error in line #" + repr(index) + " :")
        cls.errors.append("\t" + message)

    @classmethod
    def getValue(cls, source):
        return int(Loader.data[int(source)])

    @classmethod
    def setValue(cls, destination, value):
        if not Loader.isDataFull():
            Loader.data[int(destination)] = int(value)
        else:
            cls.setError(None, "Data exceeded limit size (1000)")

    @classmethod
    def assign(cls, instruction, index):
        cls.setValue(instruction.operand_3, cls.getValue(instruction.operand_1))

    @classmethod
    def let(cls, instruction, index):
        cls.setError(0, Loader.getDataIndex())
        data_index = Loader.getDataIndex()
        cls.setValue(instruction.operand_3, cls.getValue(instruction.operand_1))

    @classmethod
    def add(cls, instruction, index):
        res = cls.getValue(instruction.operand_1) + cls.getValue(instruction.operand_2)
        if len(str(abs(res))) > 10:
            cls.setError(index)
        else:
            cls.setValue(instruction.operand_3, res)

    @classmethod
    def subtract(cls, instruction, index):
        res = cls.getValue(instruction.operand_1) - cls.getValue(instruction.operand_2)
        if len(str(abs(res))) > 10:
            cls.setError(index)
        else:
            cls.setValue(instruction.operand_3, res)

    @classmethod
    def multiply(cls, instruction, index):
        res = cls.getValue(instruction.operand_1) * cls.getValue(instruction.operand_2)
        if len(str(abs(res))) > 10:
            cls.setError(index)
        else:
            cls.setValue(instruction.operand_3, res)

    @classmethod
    def divide(cls, instruction, index):
        if cls.getValue(instruction.operand_2) == 0:
            cls.setError(index, "Division by zero (0) not allowed")
        else:
            res = int(cls.getValue(instruction.operand_1) / cls.getValue(instruction.operand_2))
            if len(str(abs(res))) > 10:
                cls.setError(index)
            else:
                cls.setValue(instruction.operand_3, res)

    @classmethod
    def power(cls, instruction, index):
        res = math.pow(cls.getValue(instruction.operand_1), 2)
        if (len(str(abs(res)))) > 10:
            cls.setError(index)
        else:
            cls.setValue(instruction.operand_3, res)

    @classmethod
    def root(cls, instruction, index):
        if cls.getValue(instruction.operand_1) < 0:
            cls.setError(index, "Non real solution for square root")
        else:
            res = int(math.sqrt(cls.getValue(instruction.operand_1)))
            cls.setValue(instruction.operand_3, res)

    @classmethod
    def isEqual(cls, instruction, index):
        if cls.getValue(instruction.operand_1) == cls.getValue(instruction.operand_2):
            return int(instruction.operand_3)
        else:
            return index + 1

    @classmethod
    def isDifferent(cls, instruction, index):
        if cls.getValue(instruction.operand_1) != cls.getValue(instruction.operand_2):
            return int(instruction.operand_3)
        else:
            return index + 1

    @classmethod
    def isGreaterOrEqual(cls, instruction, index):
        if cls.getValue(instruction.operand_1) >= cls.getValue(instruction.operand_2):
            return int(instruction.operand_3)
        else:
            return index + 1

    @classmethod
    def isLess(cls, instruction, index):
        if cls.getValue(instruction.operand_1) < cls.getValue(instruction.operand_2):
            return int(instruction.operand_3)
        else:
            return index + 1

    @classmethod
    def get(cls, instruction, index):
        sub = int(instruction.operand_1) + cls.getValue(
            instruction.operand_2)  # Contiguous array means location = start + sub
        cls.setValue(instruction.operand_3, cls.getValue(sub))

    @classmethod
    def put(cls, instruction, index):
        sub = int(instruction.operand_2) + cls.getValue(
            instruction.operand_3)  # Contiguous array means location = start + sub
        cls.setValue(sub, cls.getValue(instruction.operand_1))

    @classmethod
    def loop(cls, instruction, index):
        i = cls.getValue(instruction.operand_1)
        max = cls.getValue(instruction.operand_2)
        code = int(instruction.operand_3)

        if i < max - 1:
            cls.setValue(instruction.operand_1, cls.getValue(instruction.operand_1) + 1)
            return code
        else:
            return index + 1

    @classmethod
    def print(cls, instruction, index):
        print(Fore.GREEN + "\nOutput from line #" + repr(index) + ": " +
              "{:,}".format(cls.getValue(instruction.operand_1)) + "\n" + Fore.RESET)

    @classmethod
    def read(cls, instruction, index):
        if Settings.getInputMethod() == "Manual":
            while True:
                try:
                    print(Fore.RESET + "\nEnter the value for location " + instruction.operand_3 + ": " + Fore.CYAN,
                          end='')
                    value = int(input())
                    print()
                    cls.setValue(instruction.operand_3, value)
                    index += 1
                except ValueError:
                    print(Fore.RED + "Invalid value" + Fore.RESET)
                else:
                    break
        elif Settings.getInputMethod() == "Automatic":
            cls.setValue(instruction.operand_3, cls.valueToRead)
            if cls.indexToRead < 10:
                cls.valueToRead = Loader.input[cls.indexToRead]
                cls.indexToRead += 1

    @classmethod
    def stop(cls):
        print()
        print(Fore.MAGENTA + "****************************** END OF PROGRAM *****************************")
        Settings.done = True

    @staticmethod
    def whiteSpace(string, length):
        """
        Adds whitespace every "length" characters
        :param string:
        :param length:
        :return:
        """
        return ' '.join(string[i:i + length] for i in range(0, len(string), length))

    @staticmethod
    def getVariableName(operand):
        if operand == "000":
            return "000"
        for key, value in Parser.variables.items():
            if value.get('index') == int(operand):
                return Fore.BLUE + key + Fore.RESET

    @staticmethod
    def getLabelName(operand):
        if operand == "000":
            return "000"
        for key, value in Parser.labels.items():
            if value == int(operand):
                return Fore.GREEN + key + Fore.RESET
