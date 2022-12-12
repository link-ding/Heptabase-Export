import json
import re

with open('All-Data.json path here') as json_file:
    data = json.load(json_file)
    
#print(data.keys())


def find_card(uid):
    for card in data["cardList"]:
        if card['id'] == uid:
            return '[[' + card['title'] + ']]'


pattern = r'{{card\s([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})}}'

    
for card in data["cardList"]:
    if not card["isTrashed"]:
        if '/' in card['title']:
            card['title'] = card['title'].replace('/','!')
            
        if card['title'] == '':
            continue

        match = re.findall(pattern, card['content'])
        
        for uid in match:
            link = find_card(uid)
            card["content"]= card["content"].replace("{{card "+ uid + "}}",link)
        
        path = 'export path here' + '/' +card['title']+ '.md'
        f = open(path,'w')
        f.write(card['content'])

