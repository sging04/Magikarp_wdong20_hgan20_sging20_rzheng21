from flask import Flask, session, render_template
from database import Database

app = Flask(__name__)

db = Database("database.db")

@app.route("/")
def home():
    return "Ah"

@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    pass

if __name__ == "__main__":
    app.run(debug=True)
