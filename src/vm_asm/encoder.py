"""IR -> машинный код: 3 байта на команду, little-endian."""

from typing import List

from .isa import COMMANDS, OPCODE_MASK, WORD_SIZE
from .parser import Command

BYTE_MASK = 0xFF
SHIFT_8 = 8
SHIFT_16 = 16


def _encode_word(command: Command) -> int:
    """Собирает 24-битное слово из кода и поля B."""
    spec = COMMANDS[command.mnemonic]
    word = spec.opcode & OPCODE_MASK
    if spec.has_b:
        b_mask = (1 << spec.b_bits) - 1
        word |= (command.b & b_mask) << WORD_SIZE
    return word


def encode(commands: List[Command]) -> bytes:
    """Кодирует список команд в байты (little-endian, WORD_SIZE байт)."""
    out = bytearray()
    for command in commands:
        word = _encode_word(command)
        out.append(word & BYTE_MASK)
        out.append((word >> SHIFT_8) & BYTE_MASK)
        out.append((word >> SHIFT_16) & BYTE_MASK)
    return bytes(out)