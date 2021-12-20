import json
v = "0.0.0"

with open('version.json') as f:
    info = json.load(f)
print(info["version"])

if v < info["version"]:
    print("update")

if v > info["version"]:
    print("no update")