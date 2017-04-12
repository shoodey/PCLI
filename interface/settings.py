"""
Stores the program settings
"""


class Settings:
    program = input_method = None
    done = False

    @classmethod
    def getProgram(cls):
        return cls.program

    @classmethod
    def setProgram(cls, value):
        cls.program = value

    @classmethod
    def getInputMethod(cls):
        if cls.input_method == 1:
            return "Automatic"
        elif cls.input_method == 2:
            return "Manual"

    @classmethod
    def setInputMethod(cls, value):
        cls.input_method = value
