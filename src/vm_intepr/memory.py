"""Модель памяти УВМ, основной цикл интерпретации и дамп памяти в XML."""

from typing import List
import xml.etree.ElementTree as ET

from vm_asm.isa import (
    OP_LOAD_CONST,
    OP_READ_MEM,
    OP_SHR,
    OP_WRITE_MEM,
)
from vm_asm.parser import Command

from .decoder import decode_binary

# Поле адреса B имеет ширину 18 бит => 2^18 = 262144 ячеек памяти
DATA_MEMORY_SIZE = 1 << 18
WORD_MASK_32 = 0xFFFFFFFF


class VMRuntimeError(Exception):
    """Ошибка выполнения программы в УВМ."""


class VirtualMachine:
    """Учебная виртуальная машина (Вариант №26)."""

    def __init__(self, data_size: int = DATA_MEMORY_SIZE) -> None:
        # Требование 3: память команд и память данных разделены
        self.code_memory: List[Command] = []
        self.data_memory: List[int] = [0] * data_size
        self.acc: int = 0
        self.pc: int = 0

    def load_program(self, binary: bytes) -> None:
        """Декодирует бинарный файл и загружает инструкции в память команд."""
        self.code_memory = decode_binary(binary)
        self.pc = 0

    def step(self) -> bool:
        """Выполняет одну команду. Возвращает False, если программа завершена."""
        if self.pc >= len(self.code_memory):
            return False

        cmd = self.code_memory[self.pc]
        self.pc += 1

        if cmd.a == OP_LOAD_CONST:
            assert cmd.b is not None
            self.acc = cmd.b

        elif cmd.a == OP_READ_MEM:
            self._check_addr(self.acc)
            self.acc = self.data_memory[self.acc]

        elif cmd.a == OP_WRITE_MEM:
            assert cmd.b is not None
            self._check_addr(cmd.b)
            self.data_memory[cmd.b] = self.acc

        elif cmd.a == OP_SHR:
            assert cmd.b is not None
            self._check_addr(cmd.b)
            self.acc = (self.acc & WORD_MASK_32) >> self.data_memory[cmd.b]

        else:
            raise VMRuntimeError(f"Unsupported opcode A={cmd.a}")

        return True

    def run(self) -> None:
        """Основной цикл интерпретатора."""
        while self.step():
            pass

    def _check_addr(self, addr: int) -> None:
        if not 0 <= addr < len(self.data_memory):
            raise VMRuntimeError(f"Memory access out of bounds: {addr}")

    def dump_memory_xml(self, start_addr: int, end_addr: int) -> str:
        """Формирует XML-дамп памяти данных в диапазоне [start_addr, end_addr]."""
        out_of_range = (
            start_addr < 0
            or end_addr >= len(self.data_memory)
            or start_addr > end_addr
        )
        if out_of_range:
            raise ValueError(
                f"Invalid memory dump range [{start_addr}..{end_addr}]"
            )

        root = ET.Element("memory")
        for addr in range(start_addr, end_addr + 1):
            cell = ET.SubElement(root, "cell", address=str(addr))
            cell.text = str(self.data_memory[addr])

        ET.indent(root, space="  ")
        return ET.tostring(root, encoding="unicode")