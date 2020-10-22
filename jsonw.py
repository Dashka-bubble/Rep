import json
import data


with open('inf.json', 'w') as f:
    json.dump(data.teachers, f)

with open('inf.json') as f:
    print(f.read())
