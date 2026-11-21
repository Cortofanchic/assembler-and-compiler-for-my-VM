"""CLI-интерпретатор УВМ (вариант 26).

Использование: interp.py <program.bin> <dump.xml> <start:end>
"""

import argparse
import sys
from pathlib import Path
from typing import Tuple

from vm_intepr import DecodeError, VirtualMachine, VMRuntimeError

EXIT_OK = 0
EXIT_ARG_ERROR = 1
EXIT_IO_ERROR = 2
EXIT_VM_ERROR = 3


def _parse_range(range_str: str) -> Tuple[int, int]:
    """Разбирает диапазон адресов вида 'start:end' или 'start-end'."""
    sep = ":" if ":" in range_str else "-"
    if sep not in range_str:
        raise ValueError("Range must be formatted as START:END (e.g., 0:15)")
    left, right = range_str.split(sep, maxsplit=1)
    start = int(left, 0)
    end = int(right, 0)
    if start < 0 or end < start:
        raise ValueError(f"Invalid range {start}:{end}")
    return start, end


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="UVM Interpreter (Variant 26)")
    parser.add_argument("binary", type=Path, help="input .bin program file")
    parser.add_argument("dump", type=Path, help="output .xml memory dump file")
    parser.add_argument(
        "mem_range",
        help="memory address range for dump (e.g., 10:20)",
    )
    args = parser.parse_args(argv)

    try:
        start_addr, end_addr = _parse_range(args.mem_range)
    except ValueError as exc:
        print(f"Range error: {exc}", file=sys.stderr)
        return EXIT_ARG_ERROR

    try:
        program_bytes = args.binary.read_bytes()
    except OSError as exc:
        print(f"Error reading {args.binary}: {exc}", file=sys.stderr)
        return EXIT_IO_ERROR

    vm = VirtualMachine()
    try:
        vm.load_program(program_bytes)
        vm.run()
        xml_dump = vm.dump_memory_xml(start_addr, end_addr)
    except (DecodeError, VMRuntimeError, ValueError) as exc:
        print(f"Runtime error: {exc}", file=sys.stderr)
        return EXIT_VM_ERROR

    try:
        args.dump.parent.mkdir(parents=True, exist_ok=True)
        args.dump.write_text(xml_dump + "\n", encoding="utf-8")
    except OSError as exc:
        print(f"Error writing {args.dump}: {exc}", file=sys.stderr)
        return EXIT_IO_ERROR

    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())