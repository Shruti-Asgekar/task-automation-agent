import os
import re
import sys

PATTERNS = [
    r"gsk_[A-Za-z0-9_-]{20,}",
    r"hf_[A-Za-z0-9]{20,}",
    r"sk-[A-Za-z0-9]{20,}",
    r"ghp_[A-Za-z0-9]{20,}",
    r"gho_[A-Za-z0-9]{20,}",
]

def scan():
    found = False
    for root, dirs, files in os.walk("."):
        if ".git" in root or "__pycache__" in root or ".pytest_cache" in root:
            continue
        for f in files:
            path = os.path.join(root, f)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as fp:
                    content = fp.read()
                    for pattern in PATTERNS:
                        if re.search(pattern, content):
                            print(f"SECURITY ALERT: Found pattern {pattern} in {path}", file=sys.stderr)
                            found = True
            except Exception:
                pass
    if found:
        print("Commit blocked: Secret key detected!", file=sys.stderr)
        sys.exit(1)
    else:
        print("SECRET SCAN CLEAN: No API keys or tokens found.")

if __name__ == "__main__":
    scan()
