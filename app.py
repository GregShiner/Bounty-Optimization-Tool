from flask import Flask

app = Flask(__name__)

@app.route("/authorize")
def authorize():
    return "hello"