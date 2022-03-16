from flask import Flask, request, redirect, session, render_template, url_for
from database import Database

app = Flask(__name__)

def is_logged_in():
    return "user_id" in session

@app.route("/")
def home():
    if not is_logged_in():
        return redirect(url_for("login", error="You must be logged in!"))
    return session["username"]

@app.route("/profile/<int:id>")
def profile(id):
    if not is_logged_in():
        return redirect(url_for("login", error="You must be logged in!"))

    if request.method == "GET":
        db = Database("database.db")
        username = db.fetch_username(id)

        if username is None:
            return render_template("error-redirect.html", message="Profile not found", url=url_for("home"))

        pic = db.fetch_picture(id)

        return render_template("profile.html", username=username, profile_img=pic)

    if request.method == "POST":
        return request.form["avatar"]

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
