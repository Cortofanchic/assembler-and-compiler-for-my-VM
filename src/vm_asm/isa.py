"""Описание команд учебной ВМ (вариант 26)."""

from dataclasses import dataclass

WORD_SIZE = 3

OP_READ_MEM = 0
OP_WRITE_MEM = 5
OP_LOAD_CONST = 6
OP_SHR = 7

OPCODE_MASK = 0x7


@dataclass(frozen=True)
class CommandSpec:
    """Паспорт одной команды. \n
    mnemonic - как писать комманду в ассемблере\n
    opcode - что попадёт в поле A\n
    b_bits - сколько бит отведено под поле B\n
    has_b - есть ли вообще операнд B\n
    comment - короткое пояснение, что команда делает
    """
    mnemonic: str
    opcode: int
    b_bits: int = 0
    has_b: bool = False
    comment: str = ""


COMMANDS = {
    "LOAD_CONST": CommandSpec(
        "LOAD_CONST", OP_LOAD_CONST, b_bits=12, has_b=True,
        comment="acc = B",
    ),
    "READ_MEM": CommandSpec(
        "READ_MEM", OP_READ_MEM, comment="acc = mem[acc]",
    ),
    "WRITE_MEM": CommandSpec(
        "WRITE_MEM", OP_WRITE_MEM, b_bits=18, has_b=True,
        comment="mem[B] = acc",
    ),
    "SHR": CommandSpec(
        "SHR", OP_SHR, b_bits=18, has_b=True,
        comment="acc = acc >> mem[B]",
    ),
}