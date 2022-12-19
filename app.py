import streamlit as st
import json
import zipfile
import re
import io
import uuid


st.title("Heptabase data to Obsidian Canvas")
all_data = st.file_uploader("Upload your Heptabase All-Data.json file")

if all_data is not None:
    # clean markdown data data
    data = all_data.read()
    data = json.loads(data)
    print(data.keys())

    def find_card(uid):
        for card in data["cardList"]:
            if card['id'] == uid:
                return '[[' + card['title'] + ']]'


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
                link = find_card(uid)
                card["content"]= card["content"].replace("{{card "+ uid + "}}",link)

            markdown = (card['title'],card['content'])
            markdown_list.append(markdown)
            
    zip_filename = 'cards.zip'
    zip_file = zipfile.ZipFile(zip_filename, 'w')

    for filename, contents in markdown_list:
        string_io = io.StringIO(contents)

        zip_file.writestr(filename, string_io.read())

    zip_file.close()
    
    with open(zip_filename, "rb") as fp:
          btn = st.download_button(
              label="Download Clean Cards",
              data=fp,
              file_name="Cards.zip",
              mime="application/octet-stream"
              )
          
    # export Heptabase whiteboard to canvas
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

    cards_path = st.text_input('Your Cards Path','Cards/')
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
            n['file'] = cards_path + find_card(node['cardId']) + '.md'
            result['nodes'].append(n)
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
