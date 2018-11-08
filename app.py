from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/keyboard')
def keaboard():
    keyboard = {"type" : "buttons",
                "buttons" : ['메뉴', "로또", "고양이", '영화']
                }
    return jsonify(keyboard)