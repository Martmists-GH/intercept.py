# Stdlib
import re

# External Libraries
from colorama import Fore

REGEXES = {
    "chat_event": re.compile(r"\((?P<chat>\s+?)\) (?P<author>\s+?): (?P<message>.+)")
}

CONVERT = {
    '¬w': Fore.LIGHTWHITE_EX,
    '¬W': Fore.LIGHTBLACK_EX,
    '¬R': Fore.RED,
    '¬r': Fore.LIGHTRED_EX,
    '¬G': Fore.GREEN,
    '¬g': Fore.LIGHTGREEN_EX,
    '¬B': Fore.BLUE,
    '¬b': Fore.LIGHTBLUE_EX,
    '¬y': Fore.YELLOW,
    '¬o': Fore.LIGHTYELLOW_EX,
    '¬P': Fore.CYAN,
    '¬p': Fore.LIGHTCYAN_EX,
    '¬v': Fore.MAGENTA,
    '¬V': Fore.LIGHTMAGENTA_EX,
    '¬*': Fore.RESET,
    '¬?': Fore.WHITE,
}


def without_color_codes(line: str) -> str:
    return re.sub("¬.", "", line)


def converted_color_codes(line: str) -> str:
    for k, v in CONVERT.items():
        line = line.replace(k, v)
    return line
