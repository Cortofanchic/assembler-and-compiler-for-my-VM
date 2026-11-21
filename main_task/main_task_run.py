from pathlib import Path
import subprocess
import sys
from typing import Dict, List
import xml.etree.ElementTree as ET

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

MAIN_DIR = PROJECT_ROOT / "main_task"
ASM_SCRIPT = PROJECT_ROOT / "src" / "asm.py"
INTERP_SCRIPT = PROJECT_ROOT / "src" / "intepr.py"
RESULTS_BIN_DIR = PROJECT_ROOT / "main_task" / "results_bin"
RESULTS_XML_DIR = PROJECT_ROOT / "main_task" / "results_xml"
INPUT_DIR = PROJECT_ROOT / "main_task" / "input"

TEST_CASES: Dict[str, List[int]] = {
    "vec_shr_1.asm": [128, 128, 128, 128, 4, 1, 0, 0],
    "vec_shr_2.asm": [4095, 2047, 1023, 511, 255, 15, 1, 0],
    "vec_shr_3.asm": [0, 1, 206, 0, 0, 0, 0, 2000],
}


def parse_xml_vector(xml_text: str, start_addr: int, length: int) -> List[int]:
    root = ET.fromstring(xml_text)
    cells = {
        int(cell.attrib["address"]): int(cell.text or "0")
        for cell in root.findall("cell")
    }
    return [cells[addr] for addr in range(start_addr, start_addr + length)]


def run_stage5_tests() -> None:
    MAIN_DIR.mkdir(parents=True, exist_ok=True)

    for filename, expected_vec in TEST_CASES.items():
        source_file = INPUT_DIR / filename
        stem = source_file.stem
        bin_file = RESULTS_BIN_DIR / f"{stem}.bin"
        xml_file = RESULTS_XML_DIR / f"{stem}.xml"

        print(f"<{filename}>")

        subprocess.run(
            [sys.executable, str(ASM_SCRIPT), str(source_file), str(bin_file)],
            cwd=PROJECT_ROOT,
            check=True,
        )

        subprocess.run(
            [
                sys.executable,
                str(INTERP_SCRIPT),
                str(bin_file),
                str(xml_file),
                "0:27",
            ],
            cwd=PROJECT_ROOT,
            check=True,
        )

        xml_text = xml_file.read_text(encoding="utf-8")
        print(xml_text.strip())

        actual_vec = parse_xml_vector(xml_text, start_addr=20, length=8)
        assert actual_vec == expected_vec, (
            f"{filename}: expected {expected_vec}, got {actual_vec}"
        )
        print(f"C[20..27] = {actual_vec} => OK\n")


if __name__ == "__main__":
    run_stage5_tests()