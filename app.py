import base64
import os
from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

@app.route("/gerarimagem", methods=["POST"] )
def gerarimagem():
    if request.method == "POST":
        try:
            return convertJsonToImage(request.json)
        except Exception as e:
            return jsonify({"error": str(e)})
    
def convertJsonToImage(json):
    filename = uuid.uuid4()
    generateJsonFile(json, filename)
    generateImageFile(filename)
    image = convertImageToBase64(filename)
    deleteFiles(filename)
    return image

def generateJsonFile(json, filename):
    file = open(f'{filename}.json', 'w')
    file.write(f'{json}')
    file.close()

def generateImageFile(filename):
    os.system(f'./mysql_visual_explain_cli {filename}.json {filename}.png')

def convertImageToBase64(filename):
    with open(f'{filename}.png', "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string
    
def deleteFiles(filename):
    os.remove(f'{filename}.json')
    os.remove(f'{filename}.png')