from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import json
import os 

app = Flask(__name__,template_folder="./html_app")
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/get-data")
def get_data():
    with open("./html_app/data.json","r") as datafile:
        json_data = json.load(datafile)
        datafile.close()
    data = {f"message": {json_data}}
    return jsonify(data)

if __name__ == '__main__':
    socketio.run(app, debug=True)

