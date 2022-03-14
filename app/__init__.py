from flask import Flask, request, redirect, session, render_template, url_for
from database import Database

app = Flask(__name__)

def is_logged_in():
    return "user_id" in session

@app.route("/")
def home():
    if is_logged_in():
        return session["username"]
    return "Ah"

@app.route("/battleship")
def battleship():
    return render_template("battleship.html")

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

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        error = request.args.get("error", None)
        return render_template("login.html", error=error)
    
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        db = Database("database.db")
        user_id = db.fetch_user(user, pwd)
        db.close()

        print(user_id)
        if user_id is None:
            return redirect(url_for("login", error="Incorrect credentials"))

        session["user_id"] = user_id
        session["username"] = user

        return redirect("/")

@app.route("/logout")
def logout():
    if is_logged_in():
        session.pop("user_id")
        session.pop("username")
    return redirect("/login")

if __name__ == "__main__":
    app.secret_key = "foo"
    app.run(debug=True)
