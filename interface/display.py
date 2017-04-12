import os
from . import Settings
from .colorama import *

"""
   Handles the display messages when running the program
"""


class Display:
    @classmethod
    def run(cls):
        """
        Specifies which methods to run
        """
        cls.displayWatermark()
        cls.displayProgramChoice()
        cls.separateSections()
        cls.displayInputMethod()
        cls.separateSections()

    @staticmethod
    def displayWatermark():
        """
         Display program title and authors
        """
        os.system('cls')
        display(Fore.RED + Fore.RED + Fore.RED + "Pseudo Code Language Interpreter\n")
        display(Fore.MAGENTA + "AMMINE Bassma " + Fore.BLUE + "EL AMRI Ali\n" + Fore.RESET)

    @classmethod
    def displayProgramChoice(cls):
        """
         Allows the user to input the choice of program to be ran
        """
        print(Fore.CYAN + "Available programs:")
        print("-------------------\n")
        print("(1)" + Fore.RESET + " Average of all numbers at once")
        print(Fore.CYAN + "(2)" + Fore.RESET + " Average of positive and negative numbers\n")
        while True:
            try:
                print("Enter the program number to run: " + Fore.CYAN, end='')
                value = int(input())
                if value in (1, 2):
                    Settings.setProgram(value)
                    print(Fore.GREEN + "\n=> Program has been set to (" + repr(
                        Settings.getProgram()) + ")" + Fore.RESET)
                    break
            except ValueError:
                print(Fore.RED + "Invalid value" + Fore.RESET)
            else:
                print(Fore.RED + "Invalid value (" + repr(value) + ")" + Fore.RESET)

    @classmethod
    def displayInputMethod(cls):
        """
        Allows the user to set the values input method
        """
        print(Fore.CYAN + "Available input methods:")
        print("------------------------\n")
        print("(1)" + Fore.RESET + " Automatically use values from assignment")
        print(Fore.CYAN + "(2)" + Fore.RESET + " Manually input values\n")
        while True:
            try:
                print("Enter the input method: " + Fore.CYAN, end='')
                value = int(input())
                if value in (1, 2):
                    Settings.setInputMethod(value)
                    print(Fore.GREEN + "\n=> Input method has been set to (" +
                          Settings.getInputMethod() + ")" + Fore.RESET)
                    break
            except ValueError:
                print(Fore.RED + "Invalid value" + Fore.RESET)
            else:
                print(Fore.RED + "Invalid value (" + repr(value) + ")" + Fore.RESET)

    @staticmethod
    def separateSections():
        print()
        print(Fore.RESET + "".center(os.get_terminal_size().columns, "*"))
        print()


def display(message):
    """
    Alternative print function to display centered messages
    :param message: Message to be displayed
    """
    print(message.center(os.get_terminal_size().columns))
