> You can view *.md files using a [markdown viewer](https://stackedit.io/editor).

> You can strecth the panel on the right hand to perfectly view the whole file content.

Pseudo Code Language Interpreter
============================


#### <i class="icon-users"></i> Authors

Name          | ID
------------- | ---
AMMINE Bassma | 72190
EL AMRI Ali   | 72241


----------

#### <i class="icon-code"></i> Python

Python version in use: **3.6.0**

----------

#### <i class="icon-to-end"></i> How to run

 1. Start a full screen terminal.
 2. Locate the project folder.
 3. Run `python main.py`
 4. Follow the program instructions.

----------

#### <i class="icon-cog"></i> How it works

The project includes 2 modules, each containing different classes:

> - ***Interface***
	 - **Display**: Handles the display messages when running the program
	 - **Settings**: Stores the program settings
> - ***Logic***:
	 - **File**: Scans the Pseudo Code Language file set based on settings
	 - **Instruction**: Constructs instructions from inputs
	 - **Loader**: Initializes memory with data and program
	 - **Interpreter**: Interprets the program that is loaded into memory

The main python file calls the bootstrap.
> - ***Bootstrap***: Defines running sequence of different program sections.

```sequence
Display->Display: Ask for program choice
Display->Display: Ask for input method
Display->Settings: Store given values
```

```sequence
File->File: Read file
File->Instruction: Check syntax
File->Loader: Save data to memory
File->Loader: Store program to memory
Interpreter->Loader: Read data & program
Interpreter->Interpreter: Read & test an instruction
Interpreter->Interpreter: Run the instruction
```

----------


#### <i class="icon-star"></i> Credits

 - [**Colorama**](https://github.com/tartley/colorama): Color library to prettify the terminal output.
 - [**Text Table**](https://github.com/foutaise/texttable): Text table library to nicely represent table, used to display memory (data, program and input).

----------

#### <i class="icon-cloud"></i> Github

The project is open source and available on [github](https://github.com/Shoodey/PCLI).