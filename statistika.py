import json

bilety = json.load(open("text.txt"))
j = 0
print(bilety)
for i in list(bilety.keys()):
    if bilety[i]['checked'] == 1:
        j = j+1
print('вход прошло:' + str(j))