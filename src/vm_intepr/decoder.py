"""Декодер машинного кода УВМ (3 байта, little-endian) в IR."""

from typing import List

from vm_asm.isa import *
from vm_asm.parser import Command

OPCODE_BITS = 3
OPCODE_TO_SPEC = {spec.opcode: spec for spec in COMMANDS.values()}


class DecodeError(Exception):
    """Ошибка декодирования машинного кода."""


def decode_word(word: int, byte_addr: int) -> Command:
    """Разбирает 24-битное слово на поля A и B."""
    opcode = word & OPCODE_MASK
    spec = OPCODE_TO_SPEC.get(opcode)
    if spec is None:
        raise DecodeError(f"Address {byte_addr}: unknown opcode {opcode}")

    if not spec.has_b:
        return Command(
            mnemonic=spec.mnemonic,
            a=opcode,
            b=None,
            b_raw="",
            line_no=0,
            byte_addr=byte_addr,
        )

    b_mask = (1 << spec.b_bits) - 1
    b_val = (word >> OPCODE_BITS) & b_mask
    return Command(
        mnemonic=spec.mnemonic,
        a=opcode,
        b=b_val,
        b_raw=str(b_val),
        line_no=0,
        byte_addr=byte_addr,
    )


def decode_binary(binary: bytes) -> List[Command]:
    """Декодирует байтовый поток в список команд IR."""
    if len(binary) % WORD_SIZE != 0:
        raise DecodeError(
            f"Binary size ({len(binary)} bytes) is not a multiple of {WORD_SIZE}"
        )

    commands: List[Command] = []
    for offset in range(0, len(binary), WORD_SIZE):
        chunk = binary[offset : offset + WORD_SIZE]
        word = int.from_bytes(chunk, byteorder="little")
        commands.append(decode_word(word, offset))
    return commands