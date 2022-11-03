import hashlib

bilety = {}
for i in range(200):
    #hs = hashlib.sha256(str(i+1).encode('utf-8')).hexdigest()
    hs = hashlib.sha256(str(i + 1).encode('utf-8')).hexdigest()[:24]
    bilety[hs] = {'bilet': str(i+1), 'name': 'None', 'photo': 'None', 'chat_id': 0, 'checked': 0}
print(len(bilety))
import json
json.dump(bilety, open("text.txt",'w'))
