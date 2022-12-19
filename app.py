import streamlit as st
import json
import zipfile
import re
import io
import uuid
import math


st.title("Heptabase data to Obsidian Canvas")
st.markdown("> This is a Web APP to export your Data from Heptabase to Obsidian, follow the instruction below to use.")
st.markdown("""
            1. Upload your All-Data.json file. `All-Data.json` file is in your Heptabase export folder.
            2. After you upload the file, there will be two download buttons. 
                1. Download Cards button will export all your cards in Heptabase to Markdown files in a folder with clean wiki link `[[]]`.
                2. Download Canvas button will export all your whiteboards in Heptabase to Obsidian Canvas file in a folder. You should set the Cards Path which is the cards' related path to your obsdian vault. The default path is `Cards/` 
            """)

all_data = st.file_uploader("Upload your Heptabase All-Data.json file")

if all_data is not None:
    # clean markdown data data
    data = all_data.read()
    data = json.loads(data)
    print(data.keys())

    def find_card(uid):
        for card in data["cardList"]:
            if card['id'] == uid:
                return card 


    pattern = r'{{card\s([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})}}'

    markdown_list = []
    for card in data["cardList"]:
        if not card["isTrashed"]:
            if '/' in card['title']:
                card['title'] = card['title'].replace('/','!')
                
            if card['title'] == '':
                continue

            match = re.findall(pattern, card['content'])
            
            for uid in match:
                card = find_card(uid)
                link = '[[' + card['title'] + ']]'
                card["content"]= card["content"].replace("{{card "+ uid + "}}",link)

            markdown = (card['title']+'.md',card['content'])
            markdown_list.append(markdown)
            
    zip_filename = 'cards.zip'
    zip_file = zipfile.ZipFile(zip_filename, 'w')

    for filename, contents in markdown_list:
        string_io = io.StringIO(contents)

        zip_file.writestr(filename, string_io.read())

    zip_file.close()
    
    with open(zip_filename, "rb") as fp:
          btn = st.download_button(
              label="Download Cards",
              data=fp,
              file_name="Cards.zip",
              mime="application/octet-stream"
              )
          
    # export Heptabase whiteboard to canvas

    def find_card(uid):
        for card in data["cardList"]:
            if card['id'] == uid:
                return card
            
    def find_whiteboard(uid):
        for whiteboard in data['whiteBoardList']:
            if whiteboard['id'] == uid:
                return whiteboard

    def find_cardInstance(uid):
        for card in data['cardInstances']:
            if card['id'] == uid:
                return card
            
    def detect_dirction(begin,end):
        x_diff = begin['x'] - end['x']
        y_diff = begin['y'] - end['y']

        angle = math.atan2(y_diff, x_diff)
        angle_deg = math.degrees(angle)
        print(angle_deg)
        if angle_deg > 45 and angle_deg < 135:
            return ('bottom','top')
        elif angle_deg > 135 or angle_deg < -135:
            return ('left','right')
        elif angle_deg < -45 and angle_deg > - 135:
            return ('top','bottom')
        elif angle_deg > -45 and angle_deg < 45:
            return ('right','left')
        
    def find_node(cardInstance,nodes):
        for node in nodes:
            if cardInstance['x'] == node['x'] and cardInstance['y'] == node['y']:
                return node    
            
    connections = data['connections']
    whiteboardList = data['whiteBoardList']
    sections = data['sections']

    for whiteboard in whiteboardList:
        whiteboard['nodes'] = []
        whiteboard['edges'] = []
        whiteboard['sections'] = []

    for card in data['cardInstances']:
        whiteboard_uid = card['whiteboardId']
        whiteboard = find_whiteboard(whiteboard_uid)
        whiteboard['nodes'].append(card)
        
    for connection in connections:
        whiteboard_uid = connection['whiteboardId']
        whiteboard = find_whiteboard(whiteboard_uid)
        whiteboard['edges'].append(connection)
    
    for section in sections:
        whiteboard_uid = section['whiteboardId']
        whiteboard = find_whiteboard(whiteboard_uid)
        whiteboard['sections'].append(section)

    cards_path = st.text_input('Your Cards Path','Cards/')
    def create_canvas(whiteboard):
        result = {'nodes':[],'edges':[]}
        for node in whiteboard['nodes']:
            n = {}
            n['id'] = uuid.uuid4().hex[:16]
            n['x'] = node['x']
            n['y'] = node['y']
            n['width'] = node['width']
            n['height'] = node['height']-30
            n['type'] = 'file'
            n['file'] = cards_path + find_card(node['cardId'])['title'] + '.md'
            result['nodes'].append(n)
            
        for section in whiteboard['sections']:
            n = {}
            n['id'] = uuid.uuid4().hex[:16]
            n['x'] = section['x']
            n['y'] = section['y']
            n['width'] = section['width']
            n['height'] = section['height']
            n['type'] = 'group'
            n['label'] = section['title']
            result['nodes'].append(n)
            
        for connection in whiteboard['edges']:
            if connection['beginObjectType'] == 'cardInstance' and connection['endObjectType'] == 'cardInstance':
                n = {}
                n['id'] = uuid.uuid4().hex[:16]
                begin = find_cardInstance(connection['beginId'])
                end = find_cardInstance(connection['endId'])
                n['fromNode'] = find_node(begin,result['nodes'])['id']
                n['toNode'] = find_node(end,result['nodes'])['id']
                
                toside, fromside = detect_dirction(begin,end)
                n['fromSide'] = fromside
                n['toSide'] = toside
                result['edges'].append(n)
                                       
        return result

    canvas = {}
    for whiteboard in whiteboardList:
        canvas[whiteboard['name']] = create_canvas(whiteboard)

    canvas_list = [ ]
    for key in canvas.keys(): 
        content = json.dumps(canvas[key])
        filename = key + '.canvas'
        canvas_list.append((filename,content))
              
    zip_filename = 'canvas.zip'
    zip_file = zipfile.ZipFile(zip_filename, 'w')

    for filename, contents in canvas_list:
        string_io = io.StringIO(contents)
        zip_file.writestr(filename, string_io.read())

    zip_file.close()
    
    with open(zip_filename, "rb") as fp:
          btn = st.download_button(
              label="Download Canvas",
              data=fp,
              file_name="Canvas.zip",
              mime="application/octet-stream"
              )
