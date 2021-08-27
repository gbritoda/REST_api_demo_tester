from colorama import init, Fore, Back, Style

init(convert=True)
class cPrint:
    BRIGHT_RED = Style.BRIGHT + Fore.RED
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    WHITE = Fore.WHITE
    CYAN = Fore.CYAN
    RESET = Style.RESET_ALL

    @staticmethod
    def cprint(_txt, _color=Fore.WHITE):
        print(_color + str(_txt) + cPrint.RESET)
        # print(_txt)

    @staticmethod
    def print_no_line_end(_txt, _color):
        print(_color + str(_txt) + cPrint.RESET, end=" ")

def cprint(_txt, _color= cPrint.WHITE):
    cPrint.cprint(_txt, _color)

def cprint_err(_txt):
    cPrint.cprint(_txt, cPrint.BRIGHT_RED)

def cprint_suc(_txt):
    cPrint.cprint(_txt, cPrint.GREEN)

def cprint_info(_txt):
    cPrint.cprint(_txt, cPrint.BLUE)