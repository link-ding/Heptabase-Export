import json

with open('/Users/linkding/Desktop/All-Data.json','r') as file:
    data = json.load(file)
    
#print(data.keys())


whiteboardList = data['whiteBoardList']

def find_card(uid):
	for card in data["cardList"]:
		if card['id'] == uid:
			return card

def find_cardInstance(uid):
    for card in data['cardInstances']:
        if card['id'] == uid:
            return card

def find_whiteboard(uid):
	for whiteboard in data['whiteBoardList']:
		if whiteboard['id'] == uid:
			return whiteboard

connection = data['connections'][0]


#print(data['cardInstances'][0])
begin = find_cardInstance(connection['beginId'])
end = find_cardInstance(connection['endId'])

def detect_dirction(begin,end):
    x_diff = begin['x'] - end['x']
    y_diff = begin['y'] - end['y']
    return (x_diff,y_diff)

print(detect_dirction(begin,end))



