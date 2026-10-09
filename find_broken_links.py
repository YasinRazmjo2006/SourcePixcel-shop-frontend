# find_broken_links.py
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))

# الگوهای مشکوک در فایل‌های TSX
PATTERNS = [
    (r'href=\{`([^`]*\$\{[^}]+\}[^`]*)`\}', 'href با template string'),
    (r'href=\{([a-z_][a-zA-Z0-9_.]*)\}', 'href با متغیر (ممکن است undefined باشد)'),
]

print("=" * 70)
print("Scanning for potentially broken Link hrefs...")
print("=" * 70)

issues = 0
for root, _, files in os.walk(BASE):
    if "node_modules" in root or ".next" in root or ".git" in root:
        continue

    for file in files:
        if not file.endswith((".tsx", ".ts")):
            continue

        full = os.path.join(root, file)
        rel = os.path.relpath(full, BASE)

        try:
            with open(full, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except Exception:
            continue

        for i, line in enumerate(lines, 1):
            if "<Link" not in line and "href=" not in line:
                continue

            # چک: آیا از متغیری استفاده شده که ممکن است undefined باشد؟
            m = re.search(r'href=\{([a-z_][a-zA-Z0-9_.]*)\}', line)
            if m:
                var = m.group(1)
                # فیلتر مقادیر رایج که معمولاً string هستند
                if var not in ("href", "url", "link", "path"):
                    print(f"  [{rel}:{i}] href={{{var}}}  ← suspicious")
                    issues += 1

print()
print("=" * 70)
print(f"Found {issues} suspicious lines.")
print("=" * 70)