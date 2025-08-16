import os, json

MODULES_DIR = "contents/modules"

def load_modules():
    modules = []
    for file in os.listdir(MODULES_DIR):
        if file.endswith(".json"):
            with open(os.path.join(MODULES_DIR, file), "r", encoding="utf-8") as f:
                modules.append(json.load(f))
    return modules


