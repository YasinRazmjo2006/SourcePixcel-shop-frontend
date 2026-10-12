import os

BASE = os.path.dirname(os.path.abspath(__file__))
print(f"Base: {BASE}")

# ساخت یک فایل تست
test_file = os.path.join(BASE, "test.txt")
with open(test_file, "w", encoding="utf-8") as f:
    f.write("Hello World")

print(f"Created: {test_file}")
print(f"Exists: {os.path.exists(test_file)}")