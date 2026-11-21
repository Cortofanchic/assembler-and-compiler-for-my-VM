from pathlib import Path
import subprocess
import sys

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

ASM_SCRIPT = PROJECT_ROOT / "src" / "asm.py"
INTERP_SCRIPT = PROJECT_ROOT / "src" / "intepr.py"
SOURCE_FILE = BASE_DIR / "copy_array.asm"
RESULTS_DIR = BASE_DIR / "tests_results"
XML_DIR = BASE_DIR / "tests_of_intepr"

def run_copy_array_test() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    if not SOURCE_FILE.exists():
        print(f"Can't find {SOURCE_FILE}")
        return

    name = SOURCE_FILE.stem
    bin_file = RESULTS_DIR / f"{name}.bin"
    xml_file = XML_DIR / f"{name}.xml"
    print(f"<{name}>")

    asm_res = subprocess.run(
        [sys.executable, str(ASM_SCRIPT), str(SOURCE_FILE), str(bin_file), "--test"],
        capture_output=True,
        text=True,
        check=True,
    )
    if asm_res.stdout:
        print(asm_res.stdout.strip())

    subprocess.run(
        [sys.executable, str(INTERP_SCRIPT), str(bin_file), str(xml_file), "10:23"],
        capture_output=True,
        text=True,
        check=True,
    )

    print("\nXML Dump:")
    print(xml_file.read_text(encoding="utf-8").strip())
    print("End task")


if __name__ == "__main__":
    run_copy_array_test()