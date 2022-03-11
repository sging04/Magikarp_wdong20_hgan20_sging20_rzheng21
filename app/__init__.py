from flask import Flask, session
from database import Database

app = Flask(__name__)

db = Database("database.db")

@app.route("/")
def home():
    return "Ah"

@app.route("register")
def register():
    pass

@app.route("login")
def register():
    pass

if __name__ == "__main__":
    app.run(debug=True)
