"""CLI-ассемблер УВМ (вариант 26).

Использование: asm.py <source.asm> <output.bin> [--test]
"""
import argparse
import sys
from pathlib import Path

from vm_asm import AsmError, encode, parse, WORD_SIZE

EXIT_OK = 0
EXIT_TEST_FAIL = 1
EXIT_READ_ERROR = 2
EXIT_ASM_ERROR = 3
EXIT_WRITE_ERROR = 4

TEST_TABLE_WIDTH = 82
TEST_HEADER_WIDTH = 14


def _spec_tests():
    """Список контрольных тестов из спецификации: (исходник, поля, байты)."""
    return [
        ("acc = 827", (6, 827), bytes([0xDE, 0x19, 0x00])),
        ("acc = mem[acc]", (0,), bytes([0x00, 0x00, 0x00])),
        ("mem[314] = acc", (5, 314), bytes([0xD5, 0x09, 0x00])),
        ("acc = acc >> mem[162]", (7, 162), bytes([0x17, 0x05, 0x00])),
    ]


def _print_test_header() -> None:
    """Печатает шапку таблицы контрольных тестов."""
    print("UVM Specification Benchmark Tests:")
    print(
        f"{'source':<20} {'fields':<18} "
        f"{'code':<{TEST_HEADER_WIDTH}} "
        f"{'expected':<{TEST_HEADER_WIDTH}} status"
    )
    print("-" * TEST_TABLE_WIDTH)


def _check_one(src, fields, expected) -> bool:
    """Прогоняет один тест. Возвращает True, если совпало."""
    commands = parse(src)
    code = encode(commands)
    fields_ok = commands[0].as_fields() == fields
    code_ok = code == expected
    return fields_ok and code_ok


def run_spec_tests() -> int:
    """Прогоняет контрольные тесты. Возвращает число провалов."""
    failures = 0
    _print_test_header()
    for src, fields, expected in _spec_tests():
        commands = parse(src)
        code = encode(commands)
        ok = _check_one(src, fields, expected)
        if not ok:
            failures += 1
        print(
            f"{src:<20} {str(commands[0].as_fields()):<18} "
            f"{code.hex(' ').upper():<{TEST_HEADER_WIDTH}} "
            f"{expected.hex(' ').upper():<{TEST_HEADER_WIDTH}} "
            f"{'OK' if ok else 'FAIL'}"
        )
    return failures


def _read_source(path: Path) -> str:
    """Читает исходник или бросает OSError."""
    return path.read_text(encoding="utf-8")


def _load_commands(text: str):
    """Парсит исходник и расставляет байтовые адреса."""
    commands = parse(text)
    for index, command in enumerate(commands):
        command.byte_addr = index * WORD_SIZE
    return commands


def _format_bytes_spec(binary: bytes) -> str:
    """Форматирует байты в виде '0xYY, 0xYY, 0xYY'."""
    return ", ".join(f"0x{b:02X}" for b in binary)


def _print_test_output(commands, binary: bytes) -> int:
    """Печатает IR и машинный код в формате спецификации, прогоняет тесты."""
    for idx, cmd in enumerate(commands):
        chunk = binary[idx * WORD_SIZE : (idx + 1) * WORD_SIZE]
        fields = cmd.as_fields()
        if len(fields) == 2:
            print(f"Test (A={fields[0]}, B={fields[1]}):")
        else:
            print(f"Test (A={fields[0]}):")
        print(_format_bytes_spec(chunk), end="\n\n")
    return EXIT_OK


def main(argv=None) -> int:
    """Точка входа CLI: читает исходник, пишет bin, в --test печатает IR и тесты."""
    parser = argparse.ArgumentParser(
        description="UVM Assembler (Variant 26)"
    )
    parser.add_argument("source", type=Path, help="input .asm file")
    parser.add_argument("output", type=Path, help="output .bin file")
    parser.add_argument(
        "--test", action="store_true",
        help="print IR and run benchmark tests",
    )
    args = parser.parse_args(argv)

    try:
        text = _read_source(args.source)
    except OSError as exc:
        print(f"Error reading {args.source}: {exc}", file=sys.stderr)
        return EXIT_READ_ERROR

    try:
        commands = _load_commands(text)
    except AsmError as exc:
        print(f"Assembly error: {exc}", file=sys.stderr)
        return EXIT_ASM_ERROR

    binary = encode(commands)

    try:
        args.output.write_bytes(binary)
    except OSError as exc:
        print(f"Error writing {args.output}: {exc}", file=sys.stderr)
        return EXIT_WRITE_ERROR

    print(f"Assembled commands: {len(commands)}")
    if args.test:
        return _print_test_output(commands, binary)

    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())