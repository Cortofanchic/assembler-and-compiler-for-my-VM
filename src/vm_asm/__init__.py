"""Пакет ассемблера УВМ: парсер, IR, кодировщик."""

from .encoder import encode
from .isa import COMMANDS, WORD_SIZE
from .parser import AsmError, Command, parse

__all__ = [
    "parse",
    "encode",
    "Command",
    "AsmError",
    "COMMANDS",
    "WORD_SIZE",
]