#!/usr/bin/env python3
import re
import sys
from pathlib import Path

DATE_LINE_PATTERNS = {
    "Labs": re.compile(r"\b\d{2}/\d{2}/\d{2} Labs:\s*.*Cr.*WBC.*Hgb|\b\d{2}/\d{2}/\d{2} Labs:\s*.*WBC.*Hgb.*Cr", re.I),
    "UA": re.compile(r"\b\d{2}/\d{2}/\d{2} UA:\s*.+", re.I),
    "UCx": re.compile(r"\b\d{2}/\d{2}/\d{2} UCx:\s*.+", re.I),
}

PHI_PATTERNS = [
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    re.compile(r"\b(?:MRN|DOB|Phone Number):\s*[0-9]{4,}", re.I),
    re.compile(r"\b\d{10}\b"),
]


def check_update_note(path: Path, text: str):
    issues = []
    if "Assessment:" not in text or "Plan:" not in text:
        issues.append("Missing Assessment or Plan heading.")
        return issues
    assess = text.split("Assessment:", 1)[1].split("Plan:", 1)[0].strip()
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", assess) if s.strip()]
    if not (3 <= len(sentences) <= 4):
        issues.append(f"Assessment must be 3-4 sentences; found {len(sentences)}.")
    required = [
        "consulted",
        "Cr",
        "no acute urologic intervention",
    ]
    for token in required:
        if token.lower() not in assess.lower():
            issues.append(f"Assessment missing required anchor: '{token}'.")
    return issues


def check_consult_objective(path: Path, text: str):
    issues = []
    for k, p in DATE_LINE_PATTERNS.items():
        if not p.search(text):
            issues.append(f"Missing dated {k} objective-data line.")
    return issues


def check_phi(path: Path, text: str):
    issues = []
    for pat in PHI_PATTERNS:
        if pat.search(text):
            issues.append(f"Potential PHI pattern matched: {pat.pattern}")
    return issues


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("examples/outputs")
    failures = 0
    for path in sorted(root.glob("*.md")):
        text = path.read_text()
        issues = []
        issues.extend(check_phi(path, text))
        if "update" in path.name:
            issues.extend(check_update_note(path, text))
        if "consult" in path.name:
            issues.extend(check_consult_objective(path, text))
        if issues:
            failures += 1
            print(f"FAIL {path}")
            for i in issues:
                print(f"  - {i}")
        else:
            print(f"PASS {path}")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
