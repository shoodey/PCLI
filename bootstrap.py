from interface import *
from logic import *
import os


class Bootstrap:
    @staticmethod
    def run():
        Display.run()
        File.run()

        if File.instructions:  # Not empty
            # Before the loader runs, the parser comes in to parse the
            # assembly-like code into numerical code
            # This allows u☼ to keep the same interpreter but with both
            # coding methods (assembly-like and numeric)
            Parser.run()
            if not Parser.regex_error and not Parser.parse_error:
                Loader.run()
                input("Press Enter to view memory...")
                os.system('cls')
                Display.displayWatermark()
                Loader.displayMemory()

                while True:
                    print("Do you wish to run the program? (Y/N) " + Fore.CYAN, end='')
                    value = input()
                    if value in ("Y", "y"):
                        os.system('cls')
                        Display.displayWatermark()
                        Interpreter.run()
                        Display.separateSections()
                        if len(Interpreter.errors) != 0:
                            for err in Interpreter.errors:
                                print(Fore.RED + err)
                            Display.separateSections()
                        break
                    elif value in ("N", "n"):
                        print(Fore.RED + "All this for nothing... Try it!" + Fore.RESET)
                    else:
                        print(Fore.RED + "Invalid value (" + value + ")" + Fore.RESET)

                input("Press Enter to view memory...")
                os.system('cls')
                Display.displayWatermark()
                Loader.displayMemory()

                input("Press Enter to exit...")
                os.system('cls')
                Display.displayWatermark()
                print("GOODBYE !\n")
