# LMFAO - LOLCODE Interpreter

A Python-based LOLCODE interpreter developed for **CMSC 124: Design and Implementation of Programming Languages** at the University of the Philippines Los Baños.

The project implements the fundamental stages of an interpreter, including lexical analysis, syntactic analysis, and semantic analysis, allowing users to write and execute programs using the LOLCODE programming language.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Bonus Features](#bonus-features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Interpreter](#running-the-interpreter)
- [Sample LOLCODE Program](#sample-lolcode-program)
- [Known Limitations](#known-limitations)
- [Contributors](#contributors)

## Project Overview

We created a LOLCODE interpreter, a programming language designed around internet slang and humor.

The interpreter processes LOLCODE source files through three major stages:

1. **Lexical Analysis** – Identifies and classifies lexemes into tokens.
2. **Syntactic Analysis** – Checks whether the sequence of tokens follows the language grammar and constructs an Abstract Syntax Tree (AST).
3. **Semantic Analysis and Execution** – Evaluates expressions, manages variables, performs operations, and executes program statements decoded from the AST.

The project also provides a graphical user interface (GUI) for writing, loading, and executing LOLCODE programs.

## Features

The following features are part of the base requirements outlined in the CMSC 124 project specifications.

### 1. Variables and Data Types

- Variable declaration using `I HAS A`.
- Variable initialization using `ITZ`.
- Variable reassignment using `R`.
- Support for the implicit variable `IT`.
- Dynamic typing.

Supported data types:

| Type | LOLCODE Representation |
|---|---|
| Untyped | NOOB |
| Integer | NUMBR |
| Float | NUMBAR |
| String | YARN |
| Boolean | TROOF |

### 2. Input and Output

- `VISIBLE` – Displays output to the console.
- `GIMMEH` – Accepts user input and stores it in a variable.

### 3. Operations

**Arithmetic Operations**
- `SUM OF`
- `DIFF OF`
- `PRODUKT OF`
- `QUOSHUNT OF`
- `MOD OF`
- `BIGGR OF`
- `SMALLR OF`

**Boolean Operations**
- `BOTH OF`
- `EITHER OF`
- `WON OF`
- `NOT`
- `ALL OF`
- `ANY OF`

**Comparison Operations**
- `BOTH SAEM`
- `DIFFRINT`

**String Operations**
- `SMOOSH`

### 4. Typecasting

- Explicit typecasting using `MAEK`.
- Variable recasting using `IS NOW A`.
- Implicit typecasting where supported by the language specifications.

### 5. Control Flow

**If-Then Statements**
- `O RLY?`
- `YA RLY`
- `NO WAI`
- `OIC`

**Switch-Case Statements**
- `WTF?`
- `OMG`
- `OMGWTF`
- `GTFO`
- `OIC`

**Loops**
- `IM IN YR`
- `IM OUTTA YR`
- `UPPIN`
- `NERFIN`
- `TIL`
- `WILE`

### 6. Functions

- Function declaration using `HOW IZ I`.
- Function termination using `IF U SAY SO`.
- Function calls using `I IZ`.
- Returning values using `FOUND YR`.
- Early function termination using `GTFO`.

### 7. Comments

- Single-line comments using `BTW`.
- Multiline comments using `OBTW` and `TLDR`.

## Bonus Features

The following are additional features identified in the CMSC 124 project specifications. These are beyond the minimum required implementation.

Implementation status should be updated as development progresses.

| Bonus Feature | Description |
|---|---|
| MEBBE | Else-if clauses in conditional statements. |
| If-Else Nesting | Allows conditional statements inside other conditional statements. |
| Switch Nesting | Allows switch-case statements inside other switch-case statements. |
| Nested Control Statements | Allows different flow-control structures to be nested within one another. |
| Loop Nesting | Allows loops to be placed inside other loops. |

## Project Structure

The project is organized into separate modules for the interpreter and graphical user interface.

```text
CMSC-124-LOLCODE--LMFAO/
│
├── source code/
│   ├── interpreter/
│   │   ├── test_cases/
│   │   ├── ast_nodes.py
│   │   ├── grammars.py
│   │   ├── interpreter.py
│   │   ├── lex_analyzer.py
│   │   ├── lexemes.py
│   │   ├── parser.py
│   │   ├── symbol_table.py
│   │   ├── tokens.py
│   │   ├── typecast.py
│   │   └── values.py
│   │
│   └── gui/
│       └── gui.py
│
├── main.py
├── README.md
└── ...
```

## Requirements

- Python 3.x
- PyQt6

## Installation

1. Clone or download the repository.

```bash
git clone https://github.com/yssenen-beep/CMSC-124-LOLCODE--LMFAO.git
```

2. Navigate to the project directory.

```bash
cd CMSC-124-LOLCODE--LMFAO/source\ code
```

3. Set up python virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate
```


3. Install the required dependencies.

```bash
pip install -r requirements.txt
```

4. Install the required dependencies.

```bash
python3 main.py
```

5. Now you can run any program you want

## Running the Interpreter

Run the main entry point from the project root directory:

```bash
python3 main.py
```

The graphical user interface should launch, allowing users to load, edit, and execute LOLCODE source files.

LOLCODE source files should use the `.lol` file extension but we also allow other files to be loaded into the parser.

## Sample LOLCODE Program

The following is a simple example demonstrating variable declaration, arithmetic operations, and output.

```lolcode
HAI

WAZZUP
    I HAS A num1 ITZ 10
    I HAS A num2 ITZ 20
    I HAS A result
BUHBYE

result R SUM OF num1 AN num2

VISIBLE "The result is:"
VISIBLE result

KTHXBYE
```

Expected output:

```text
The result is:
30
```

## Known Limitations

The interpreter is subject to the language constructs and implementation scope defined in the CMSC 124 project specifications.

The following are not necessarily supported:

- Features not included in the base project requirements.
- Additional LOLCODE language constructs not explicitly implemented.
- Bonus features that aren't listed in this READ.md

Refer to the Bonus Features section for the current implementation status of additional functionality.

## Contributors

Developed by:

- Bart Greg R. Jabeguero
- Kevin Aaron A. Salazar
- Yvan Luis Senen
- Jeri Lian G. Estabillo

**Course:** CMSC 124 – Design and Implementation of Programming Languages  
**Institution:** University of the Philippines Los Baños  
**Academic Year:** First Semester, AY 2026–2027
