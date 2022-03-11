from flask import Flask, request, redirect, session, render_template, url_for
from database import Database

app = Flask(__name__)

@app.route("/")
def home():
    return "Ah"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        error = request.args.get("error", None)
        return render_template("register.html", error=error)

    if request.method == 'POST':

        user = request.form["username"]
        pwd = request.form["password"]

        db = Database("database.db")
        success = db.register_user(user, pwd)
        db.close()

        if success:
            return redirect("/login")
        else:
            return redirect(url_for("register", error="User already exists"))

@app.route("/login")
def login():
    pass

if __name__ == "__main__":
    app.run(debug=True)
