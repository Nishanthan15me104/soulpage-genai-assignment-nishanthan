# save as clear_cache.py and run: python clear_cache.py
import pathlib
import shutil

# Find all __pycache__ folders
for path in pathlib.Path(".").rglob("__pycache__"):
    print(f"Deleting {path}...")
    shutil.rmtree(path)
print("Cache cleared! Now try running your server.")