from interface import *
from . import File
from . import Instruction
import re

"""
    Parses assembly-like code into numeric if any
"""


class Parser:
    needsParsing = False
    variables = {}
    labels = {}
    instructions = []
    regex_error = []
    parse_error = None
    program = []  # For display purposes only

    @classmethod
    def run(cls):
        """
        Specifies which methods to run
        """
        cls.detect()
        Display.separateSections()
        if cls.needsParsing:
            cls.firstPass()
            if cls.regex_error:
                print(Fore.CYAN + "Parser Check:")
                print("-------------" + Fore.RESET)
                print(Fore.RED + "\n(!) Unexpected variable name in line " +
                      repr(cls.regex_error[1] + 1) + ": " +
                      cls.regex_error[0] + Fore.RESET)
                Display.separateSections()
            else:
                cls.secondPass()
                if cls.parse_error:
                    print(Fore.CYAN + "Parser Check:")
                    print("-------------" + Fore.RESET)
                    print(Fore.RED + "\n(!) Variable declaration not found in line " +
                          repr(cls.parse_error + 1) + "." + Fore.RESET)
                    Display.separateSections()

    @classmethod
    def detect(cls):
        for instruction in File.instructions:
            if instruction.isAssemblyLike():
                cls.needsParsing = True
                break

        if cls.needsParsing:
            print(Fore.CYAN + "Language Check:")
            print("---------------" + Fore.RESET)
            print(Fore.GREEN + "\n(+) Assembly-like code detected." + Fore.RESET)
        else:
            print(Fore.CYAN + "Language Check:")
            print("---------------" + Fore.RESET)
            print(Fore.GREEN + "\n(+) Numerical code detected." + Fore.RESET)

    @classmethod
    def firstPass(cls):
        """
        Iterates on the code to store all the vars, the data and the labels
        Checks if var name respect ([A-Z])([A-Z0-9]){1,3}
        :return:
        """
        variable_index = 0
        found_var = False
        iterator = 0
        for instruction in File.instructions:
            if not cls.isValid(instruction, iterator):
                break
            if instruction.operator == "VAR":
                cls.variables.update({
                    instruction.operand_1: {
                        'size': int(instruction.operand_2),
                        'index': int(variable_index),
                        'elements': []
                    }
                })
                variable_index += int(instruction.operand_2)
                found_var = instruction
            elif instruction.operator == "START":
                label_location = 0
            elif instruction.isAssemblyLike():
                found_var = False
                if instruction.operator == "LBL":
                    cls.labels.update({instruction.operand_1: label_location - len(cls.labels)})
                label_location += 1
            else:
                if found_var:
                    cls.variables.get(found_var.operand_1).get('elements').append(
                        int(instruction.stream.replace(" ", "")))
            iterator += 1
        cls.fillData()

    @classmethod
    def secondPass(cls):
        """
        Iterates on the code to check if all vars an labels exist
        Translate instructions to numerical values
        :return:
        """
        iterator = 0
        for instruction in File.instructions:
            if instruction.isAssemblyLike():
                if instruction.operator == "START" or instruction.operator == "END":
                    cls.instructions.append(Instruction("+9 999 999 999"))
                elif instruction.operator == "LBL":
                    pass  # We do not parse the LBL instruction, we just map it
                    # cls.instructions.append(Instruction(
                    #     Instruction.operators.get(instruction.operator) + " " +
                    #     repr(cls.labels.get(instruction.operand_1)).zfill(3) +
                    #     " 000 000"
                    # ))
                elif instruction.operator == "VAR":
                    pass
                elif instruction.operator == "GEQ" or instruction.operator == "LSS" or instruction.operator == "ITJ":
                    cls.program.append(instruction)  # To display unparsed instruction
                    if (instruction.operand_1 == "000" or instruction.operand_1 in cls.variables) and \
                            (instruction.operand_2 == "000" or instruction.operand_2 in cls.variables) and \
                            (instruction.operand_3 == "000" or instruction.operand_3 in cls.labels):
                        i1 = repr(cls.variables.get(instruction.operand_1).get('index')).zfill(3)
                        i2 = repr(cls.variables.get(instruction.operand_2).get('index')).zfill(3)
                        i3 = repr(cls.labels.get(instruction.operand_3)).zfill(3)
                        cls.instructions.append(Instruction(
                            Instruction.operators.get(instruction.operator) + " " + i1 + " " + i2 + " " + i3
                        ))
                    else:
                        cls.parse_error = iterator
                        break
                else:
                    cls.program.append(instruction)  # To display unparsed instruction
                    if (instruction.operand_1 == "000" or instruction.operand_1 in cls.variables) and \
                            (instruction.operand_2 == "000" or instruction.operand_2 in cls.variables) and \
                            (instruction.operand_3 == "000" or instruction.operand_3 in cls.variables):

                        if instruction.operand_1 != "000":
                            i1 = repr(cls.variables.get(instruction.operand_1).get('index')).zfill(3)
                        else:
                            i1 = "000"

                        if instruction.operand_2 != "000":
                            i2 = repr(cls.variables.get(instruction.operand_2).get('index')).zfill(3)
                        else:
                            i2 = "000"

                        if instruction.operand_3 != "000":
                            i3 = repr(cls.variables.get(instruction.operand_3).get('index')).zfill(3)
                        else:
                            i3 = "000"

                        cls.instructions.append(Instruction(
                            Instruction.operators.get(instruction.operator) + " " + i1 + " " + i2 + " " + i3
                        ))
                    else:
                        cls.parse_error = iterator
                        break
            iterator += 1
        last_line = File.instructions[-1].stream.replace(" ", "")
        cls.instructions.append(Instruction(
            last_line[0:2] + " " + cls.whiteSpace(last_line[2:11], 3)
        ))

    @classmethod
    def fillData(cls):
        for key, value in cls.variables.items():
            for index in range(0, value.get('size')):
                # Case 1: No initialization: value = 0
                if not value.get('elements'):
                    cls.instructions.append(Instruction(
                        Instruction.operators.get('ASG') + " " +
                        cls.whiteSpace("0".zfill(9), 3)
                        # We directly use the assign operator and parse the instruction
                        # with zero fill to 9 characters and spacing every 3 characters
                        # e.g. +0 000 000 010, +0 000 000 001, ...
                    ))
                # Case 2.1: Some are initialized
                if index < len(value.get('elements')):
                    cls.instructions.append(Instruction(
                        Instruction.operators.get('ASG') + " " +
                        cls.whiteSpace(repr(value.get('elements')[index]).zfill(9), 3)
                    ))
                # Case 2.2: Fill the rest with the firs value
                if index >= len(value.get('elements')) and value.get('elements'):
                    cls.instructions.append(Instruction(
                        Instruction.operators.get('ASG') + " " +
                        cls.whiteSpace(repr(value.get('elements')[0]).zfill(9), 3)
                    ))

    @classmethod
    def isValid(cls, instruction, iterator):
        """
        Checks if all operands are valid
        Rules: - 2 to 4 character long alphanumeric symbols
               - One alphabetic character followed by 1 to 3 alphanumeric symbols
               - The characters must be upper case, i.e. A-Z; the digits are 0-9
        :param iterator:
        :param instruction:
        :return:
        """

        if instruction.isAssemblyLike():
            if instruction.operator == "LBL" or instruction.operator == "VAR":
                if instruction.operand_1 != re.search("([A-Z])([A-Z0-9]){1,3}", instruction.operand_1).group():
                    cls.regex_error = [instruction.operand_1, iterator]
                    return False
            elif instruction.operator != "START" and instruction.operator != "END":
                if instruction.operand_1 != "000":
                    if instruction.operand_1 != re.search("([A-Z])([A-Z0-9]){1,3}", instruction.operand_1).group():
                        cls.regex_error = [instruction.operand_1, iterator]
                        return False
                if instruction.operand_2 != "000":
                    if instruction.operand_2 != re.search("([A-Z])([A-Z0-9]){1,3}", instruction.operand_2).group():
                        cls.regex_error = [instruction.operand_2, iterator]
                        return False
                if instruction.operand_3 != "000":
                    if instruction.operand_3 != re.search("([A-Z])([A-Z0-9]){1,3}", instruction.operand_3).group():
                        cls.regex_error = [instruction.operand_3, iterator]
                        return False
        return True

    @staticmethod
    def whiteSpace(string, length):
        """
        Adds whitespace every "length" characters
        :param string:
        :param length:
        :return:
        """
        return ' '.join(string[i:i + length] for i in range(0, len(string), length))
