"""Разбор текста ассемблера (алгебраический синтаксис) в IR."""

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from .isa import COMMANDS, WORD_SIZE

COMMENT_MARKERS = (";", "//")
METACHAR = ":"

RE_READ_MEM = re.compile(r"^acc\s*=\s*mem\[\s*acc\s*\]$", re.IGNORECASE)
RE_LOAD_CONST = re.compile(r"^acc\s*=\s*(.+)$", re.IGNORECASE)
RE_WRITE_MEM = re.compile(r"^mem\[\s*(.+?)\s*\]\s*=\s*acc$", re.IGNORECASE)
RE_SHR = re.compile(
    r"^acc\s*(?:=\s*acc\s*>>|>>=)\s*mem\[\s*(.+?)\s*\]$", re.IGNORECASE
)


@dataclass
class Command:
    """Одна команда в IR: мнемоника, поля A и B, строка исходника, адрес."""
    mnemonic: str
    a: Optional[int]
    b: Optional[int]
    b_raw: str
    line_no: int
    byte_addr: int = 0

    def as_fields(self):
        """Поля команды в виде кортежа: (A,) или (A, B)."""
        if self.b is None:
            return (self.a,)
        return (self.a, self.b)


class AsmError(Exception):
    """Ошибка ассемблирования."""


def _strip_comment(line: str) -> str:
    """Отрезает комментарий (';' или '//') и хвостовые пробелы."""
    for marker in COMMENT_MARKERS:
        index = line.find(marker)
        if index != -1:
            line = line[:index]
    return line.rstrip()


def _is_label_name(text: str) -> bool:
    """True, если text похож на имя метки (буква/подчёркивание + alnum)."""
    if not text:
        return False
    body = text.replace("_", "a")
    if not body.isalnum():
        return False
    return text[0].isalpha() or text[0] == "_"


def _cut_labels(line: str, labels: Dict[str, int], byte_addr: int) -> str:
    """Снимает ведущие метки 'name:' и запоминает их адреса. Возвращает остаток."""
    while True:
        colon = line.find(METACHAR)
        if colon == -1:
            return line
        head = line[:colon].strip()
        if not _is_label_name(head):
            return line
        labels[head] = byte_addr
        line = line[colon + 1:].strip()


def _collect_labels(source: str) -> Tuple[Dict[str, int], List[Tuple[int, str]]]:
    """Первый проход: собирает метки, возвращает (labels, [(line_no, line)])."""
    labels: Dict[str, int] = {}
    clean: List[Tuple[int, str]] = []
    command_index = 0

    for line_no, raw in enumerate(source.splitlines(), start=1):
        line = _strip_comment(raw).strip()
        if not line:
            continue
        byte_addr = command_index * WORD_SIZE
        line = _cut_labels(line, labels, byte_addr)
        if not line:
            continue
        clean.append((line_no, line))
        command_index += 1

    return labels, clean


def parse(source: str) -> List[Command]:
    """Разбирает исходник в список Command. Метки -> байтовые адреса."""
    labels, clean = _collect_labels(source)
    return [_parse_line(no, ln, labels) for no, ln in clean]


def _build_command(
    line_no: int, mnemonic: str, raw_b: Optional[str], labels: Dict[str, int]
) -> Command:
    """Создает объект Command по имени внутренней мнемоники и сырому операнду."""
    spec = COMMANDS[mnemonic]
    if not spec.has_b:
        return Command(mnemonic, spec.opcode, None, "", line_no)
    assert raw_b is not None
    value = _resolve(line_no, raw_b.strip(), labels, spec.b_bits)
    return Command(mnemonic, spec.opcode, value, raw_b.strip(), line_no)


def _parse_line(line_no: int, line: str, labels: Dict[str, int]) -> Command:
    """Разбирает одну строку с алгебраическим синтаксисом."""
    if RE_READ_MEM.match(line):
        return _build_command(line_no, "READ_MEM", None, labels)

    match = RE_SHR.match(line)
    if match:
        return _build_command(line_no, "SHR", match.group(1), labels)

    match = RE_WRITE_MEM.match(line)
    if match:
        return _build_command(line_no, "WRITE_MEM", match.group(1), labels)

    match = RE_LOAD_CONST.match(line)
    if match:
        return _build_command(line_no, "LOAD_CONST", match.group(1), labels)

    raise AsmError(f"Line {line_no}: invalid syntax '{line}'")


def _resolve(line_no: int, token: str, labels: Dict[str, int], bits: int) -> int:
    """Возвращает число по операнду: десятичное, 0x.. или метка (@name)."""
    if token.startswith("@"):
        token = token[1:]
    if token in labels:
        value = labels[token]
    else:
        try:
            value = int(token, 0)
        except ValueError:
            raise AsmError(
                f"Line {line_no}: operand '{token}' is neither a number nor a label"
            )
    if not 0 <= value < (1 << bits):
        raise AsmError(
            f"Line {line_no}: {value} does not fit into {bits}-bit field B"
        )
    return value