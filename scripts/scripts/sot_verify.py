import argparse
import json
import os
import re
from pathlib import Path

def extract_sections(spec_path: Path, start: int, end: int):
    with open(spec_path, "r", encoding="utf-8") as f:
        text = f.read()

    sections = {}
    for i in range(start, end + 1):
        pattern = rf"## {i}\) (.*?)\n(.*?)(?=\n## \d\)|\Z)"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            sections[i] = match.group(0).strip()
        else:
            print(f"[ERROR] Missing section {i} in {spec_path}")
            return None
    return sections

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", required=True, help="Path to spec file")
    parser.add_argument("--sections", required=True, help="Range, e.g., 2..10")
    parser.add_argument("--schema", required=True, help="Path to JSON schema")
    args = parser.parse_args()

    spec_path = Path(args.spec)
    schema_path = Path(args.schema)

    if not spec_path.exists():
        print(f"[FAIL] Spec file not found: {spec_path}")
        exit(2)
    if not schema_path.exists():
        print(f"[FAIL] Schema file not found: {schema_path}")
        exit(2)

    start, end = map(int, args.sections.split(".."))
    sections = extract_sections(spec_path, start, end)
    if not sections:
        print("[FAIL] Required sections missing or not parseable")
        exit(2)

    print(f"[PASS] Extracted sections {start} to {end} from {spec_path.name}")
    print(f"[PASS] Schema file exists: {schema_path.name}")
    exit(0)

if __name__ == "__main__":
    main()
