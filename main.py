import sys
from colorama import Fore, Style, init
from app.calculator import Calculator
from app.input_validators import InputValidator
from app.operations import OperationFactory
from app.exceptions import CalculatorError
from app.logger import Logger

init(autoreset=True)
logger = Logger.get_logger()

def dynamic_help_menu(func):
    def wrapper(*args, **kwargs):
        print(f"\n{Fore.CYAN}--- Enhanced Calculator CLI Help ---{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Arithmetic Commands:{Style.RESET_ALL}")
        ops = OperationFactory.list_supported_operations()
        for op in ops:
            print(f"  {op:<12} <num1> <num2>")
        print(f"\n{Fore.YELLOW}History and Control Commands:{Style.RESET_ALL}")
        print("  history      - Display calculation history")
        print("  undo         - Revert last calculation")
        print("  redo         - Redo last undone calculation")
        print("  clear        - Clear in-memory history")
        print("  save         - Save calculation history to CSV")
        print("  load         - Load calculation history from CSV")
        print("  help         - Display available commands")
        print("  exit         - Exit application\n")
        return func(*args, **kwargs)
    return wrapper

@dynamic_help_menu
def show_help():
    pass

def start_repl():
    calc = Calculator()
    print(f"{Fore.GREEN}=== Enhanced Calculator Application ==={Style.RESET_ALL}")
    print("Type 'help' for commands or 'exit' to quit.\n")

    while True:
        try:
            raw_input_line = input(f"{Fore.BLUE}calc > {Style.RESET_ALL}").strip()
            if not raw_input_line:
                continue

            tokens = raw_input_line.split()
            cmd = tokens[0].lower()

            if cmd == "exit":
                print(f"{Fore.GREEN}Exiting application.{Style.RESET_ALL}")
                break
            elif cmd == "help":
                show_help()
            elif cmd == "history":
                history = calc.get_history()
                if not history:
                    print(f"{Fore.YELLOW}History is empty.{Style.RESET_ALL}")
                else:
                    for idx, item in enumerate(history, 1):
                        print(f"{idx}. {item}")
            elif cmd == "undo":
                if calc.undo():
                    print(f"{Fore.GREEN}Last calculation undone.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}Nothing to undo.{Style.RESET_ALL}")
            elif cmd == "redo":
                if calc.redo():
                    print(f"{Fore.GREEN}Redo successful.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}Nothing to redo.{Style.RESET_ALL}")
            elif cmd == "clear":
                calc.clear()
                print(f"{Fore.GREEN}History cleared.{Style.RESET_ALL}")
            elif cmd == "save":
                calc.save()
                print(f"{Fore.GREEN}History saved.{Style.RESET_ALL}")
            elif cmd == "load":
                calc.load()
                print(f"{Fore.GREEN}History loaded.{Style.RESET_ALL}")
            elif cmd in OperationFactory.list_supported_operations():
                if len(tokens) != 3:
                    print(f"{Fore.RED}Error: Operation '{cmd}' requires exactly two numbers.{Style.RESET_ALL}")
                    continue
                a, b = InputValidator.validate_operands(tokens[1], tokens[2])
                result_calc = calc.calculate(cmd, a, b)
                print(f"{Fore.GREEN}Result: {result_calc.format_result()}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Unknown command: '{cmd}'. Type 'help' for instructions.{Style.RESET_ALL}")

        except CalculatorError as err:
            logger.warning(f"Error encountered: {str(err)}")
            print(f"{Fore.RED}Error: {str(err)}{Style.RESET_ALL}")
        except (KeyboardInterrupt, EOFError):  # pragma: no cover
            print(f"\n{Fore.GREEN}Session terminated.{Style.RESET_ALL}")
            break
        except Exception as ex:  # pragma: no cover
            logger.error(f"Unexpected internal error: {str(ex)}")
            print(f"{Fore.RED}Unexpected internal error: {str(ex)}{Style.RESET_ALL}")

if __name__ == "__main__":
    start_repl()  # pragma: no cover
