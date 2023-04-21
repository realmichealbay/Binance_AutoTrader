from flask import Flask, render_template
from flask_socketio import SocketIO
import os
app = Flask(__name__,template_folder="P:\Mass Storage 1\Creative stuff\Vs Code\Binance_AutoTrader\html")
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    socketio.run(app, debug=True)

