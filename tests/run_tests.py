import glob
import os
import subprocess


os.makedirs("tests_results", exist_ok=True)
files = sorted(glob.glob("spec_*.asm")) + (["demo.asm"] if os.path.exists("demo.asm") else [])

for f in files:
    name = os.path.splitext(f)[0]
    print(f"<{name}>")
    res = subprocess.run(
        ["python", "../src/asm.py", f, f"tests_results/{name}.bin", "--test"],
        capture_output=True, text=True, check=True
    )
    lines = res.stdout.splitlines()
    print("\n".join(lines))

print("End task")