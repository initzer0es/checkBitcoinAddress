from colorama import init, AnsiToWin32, Fore, Back, Style
import platform


DIRECTORY_SEPARATOR = '/' if 'linux' == platform.system().lower() else '\\'


def colorama_init():
    if (DIRECTORY_SEPARATOR == '\\'):
        init()


class Color:
    bBlack = Back.BLACK
    bBlue = Back.BLUE
    bCyan = Back.CYAN
    bGreen = Back.GREEN
    bLBlack = Back.LIGHTBLACK_EX
    bLBlue = Back.LIGHTBLUE_EX
    bLCyan = Back.LIGHTCYAN_EX
    bLGreen = Back.LIGHTGREEN_EX
    bLMagenta = Back.LIGHTMAGENTA_EX
    bLRed = Back.LIGHTRED_EX
    bLWhite = Back.LIGHTWHITE_EX
    bLYellow = Back.LIGHTYELLOW_EX
    bMagenta = Back.MAGENTA
    bRed = Back.RED
    bWhite = Back.WHITE
    bYellow = Back.YELLOW
    black = Fore.BLACK
    blue = Fore.BLUE
    cyan = Fore.CYAN
    green = Fore.GREEN
    lBlack = Fore.LIGHTBLACK_EX
    lBlue = Fore.LIGHTBLUE_EX
    lCyan = Fore.LIGHTCYAN_EX
    lGreen = Fore.LIGHTGREEN_EX
    lMagenta = Fore.LIGHTMAGENTA_EX
    lRed = Fore.LIGHTRED_EX
    lWhite = Fore.LIGHTWHITE_EX
    lYellow = Fore.LIGHTYELLOW_EX
    magenta = Fore.MAGENTA
    red = Fore.RED
    sReset = Style.RESET_ALL
    white = Fore.WHITE
    yellow = Fore.YELLOW
