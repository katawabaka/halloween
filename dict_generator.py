import hashlib

bilety = {}
for i in range(200):
    hs = hashlib.sha256(str(i+1).encode('utf-8')).hexdigest()
    bilety[hs] = {'bilet': str(i+1), 'name': 'None', 'photo': 'None', 'chat_id': 0}

import json
json.dump(bilety, open("text.txt",'w'))
