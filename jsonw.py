import json
import data
dict1={}
for i,j in data.goals.items():
    dict1[i]=j
    print(dict1)
list =[]
list.append(dict1); print(list)
list.append(data.teachers); print(list)
with open('inf.json', 'w') as f:
    json.dump(list, f)




with open('inf.json') as f:
    print(f.read())
