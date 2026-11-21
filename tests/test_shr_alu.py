from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

ASM_SCRIPT = PROJECT_ROOT / "src" / "asm.py"
INTERP_SCRIPT = PROJECT_ROOT / "src" / "intepr.py"
SOURCE_FILE = BASE_DIR / "shr_alu.asm"


def run_alu_test() -> None:
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    bin_file = BASE_DIR / "tests_results" / "shr_alu.bin"
    xml_file = BASE_DIR / "tests_of_intepr" / "shr_alu.xml"

    subprocess.run(
        [sys.executable, str(ASM_SCRIPT), str(SOURCE_FILE), str(bin_file)],
        cwd=PROJECT_ROOT,
        check=True,
    )

    subprocess.run(
        [sys.executable, str(INTERP_SCRIPT), str(bin_file), str(xml_file), "314:315"],
        cwd=PROJECT_ROOT,
        check=True,
    )

    xml_text = xml_file.read_text(encoding="utf-8")
    print(xml_text.strip())

    root = ET.fromstring(xml_text)
    actual = {
        int(cell.attrib["address"]): int(cell.text or "0")
        for cell in root.findall("cell")
    }


if __name__ == "__main__":
    run_alu_test()