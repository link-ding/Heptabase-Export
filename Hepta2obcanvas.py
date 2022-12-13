import json
import uuid

print()

with open('your All-Data.json path here') as json_file:
    data = json.load(json_file)
    
print(data.keys())


def find_card(uid):
    for card in data["cardList"]:
        if card['id'] == uid:
            return card['title']

def find_whiteboard(uid):
    for whiteboard in data['whiteBoardList']:
        if whiteboard['id'] == uid:
            return whiteboard

whiteboardList = data['whiteBoardList']


for whiteboard in whiteboardList:
    whiteboard['nodes'] = []

for card in data['cardInstances']:
    whiteboard_uid = card['whiteboardId']
    whiteboard = find_whiteboard(whiteboard_uid)
    whiteboard['nodes'].append(card)


def create_canvas(whiteboard):
    result = {'nodes':[]}
    for node in whiteboard['nodes']:
        n = {}
        n['id'] = uuid.uuid4().hex[:16]
        n['x'] = node['x']
        n['y'] = node['y']
        n['width'] = node['width']
        n['height'] = node['height']
        n['type'] = 'file'
        n['file'] = "Your Cards path here" + find_card(node['cardId']) + '.md'
        result['nodes'].append(n)
    return result

canvas = {}
for whiteboard in whiteboardList:
    canvas[whiteboard['name']] = create_canvas(whiteboard)

for key in canvas.keys():
    with open(key + '.canvas','w') as file:
        json_string = json.dumps(canvas[key])
        file.write(json_string)


