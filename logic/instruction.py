""""
Constructs instructions from inputs
"""


class Instruction:
    operators = {
        'ASG': '+0', 'VAR': '-0',
        'ADD': '+1', 'SUB': '-1',
        'MUL': '+2', 'DIV': '-2',
        'SQR': '+3', 'QRT': '-3',
        'EQU': '+4', 'NEQ': '-4',
        'GEQ': '+5', 'LSS': '-5',
        'ARR': '+6', 'ARW': '-6',
        'ITJ': '+7', 'LBL': '-7',
        'INP': '+8', 'OUT': '-8',
        'STP': '+9'
    }

    def __init__(self, stream):
        """
        Initializes an instruction along its different key parts
        :param stream: string input to be "tokenized"
        """
        self.stream = stream
        self.tokens = stream.split()

        self.operator = self.tokens[0]
        self.operand_1 = None
        self.operand_2 = None
        self.operand_3 = None

        if len(self.tokens) > 1:
            self.operand_1 = self.tokens[1]
        if len(self.tokens) > 2:
            self.operand_2 = self.tokens[2]
        if len(self.tokens) > 3:
            self.operand_3 = self.tokens[3]

    def isAssemblyLike(self):
        return self.operator in self.operators \
               or self.operator == "START" \
               or self.operator == "END"

    def isValid(self):
        """
        Checks if operand is valid and if tokens' length does not exceed 4
        :return: returns true if valid, otherwise returns false
        """

        return (self.isAssemblyLike() or self.operator in self.operators.values()) \
               and len(self.tokens) <= 4
