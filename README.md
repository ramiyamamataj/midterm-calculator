# Enhanced Calculator Command-Line Application

## Project Description
A command-line interface (REPL) calculator developed in Python implementing Object-Oriented Programming and design patterns:
- Factory Design Pattern: Dynamically creates arithmetic operations in `app/operations.py`.
- Memento Design Pattern: Preserves calculation history state for `undo` and `redo` execution in `app/calculator_memento.py`.
- Observer Design Pattern: Manages logging and CSV auto-saving via pandas in `app/calculator.py`.
- Decorator Pattern: Generates a dynamic help menu based on registered operations in `main.py`.
- Colorama: Provides formatted terminal feedback.

## Installation and Setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/ramiyamamataj/midterm-calculator.git](https://github.com/ramiyamamataj/midterm-calculator.git)
   cd midterm-calculator