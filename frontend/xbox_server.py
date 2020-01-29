from flask import Flask

app = Flask(SpaceHawks_Xbox_Server)

@app.route("/")
def hello():
    return "Hello"
