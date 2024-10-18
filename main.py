from flask import Flask, redirect, render_template, request, session, url_for
import hashlib
from db import get_strokes, get_usernames, check_password, get_userid

app = Flask(__name__)
app.config["SECRET_KEY"] = "aasntuhea"


def calculateGross(handicap, tee, stableford_points):
    strokes = get_strokes(tee, handicap)
    return str(72 + strokes + (36 - stableford_points))


@app.route("/")
def home():
    if not session.get("logged_in"):
        session["logged_in"] = False

    return render_template("index.html")


@app.route("/calculate",  methods=["POST", "GET"])
def calculate():
    if request.method == "POST":
        tee = request.form.get("tee")
        stableford_points = request.form.get("stableford_points")
        handicap = request.form.get("handicap")

        print(tee, stableford_points, handicap)
        if not stableford_points:
            return render_template("calculate.html",
                                   error="Please enter your stableford points.",
                                   tee=tee,
                                   handicap=handicap)

        if not handicap:
            return render_template("calculate.html",
                                   error="Please enter your handicap",
                                   tee=tee,
                                   handicap=handicap)

        # calculation
        gross = calculateGross(float(handicap), tee, int(stableford_points))

        return render_template("calculate.html",
                               tee=tee,
                               stableford_points=stableford_points,
                               handicap=handicap,
                               gross=gross)

    return render_template("calculate.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        submit = request.form.get('submit')

        if submit:
            print("probleem")

        if not username or username not in get_usernames():
            return render_template("login.html",
                                   error="Invalid username")

        password = hashlib.sha256(
            (request.form.get('password') + username).encode()).hexdigest()

        check_p = check_password(username, password)
        if not check_p:
            return render_template("login.html",
                                   error="Invalid username or password")
        if check_p:
            session["username"] = username
            session["user_id"] = get_userid(username)
            session["logged_in"] = True
            return redirect(url_for('rounds'))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return render_template("logout.html")


@app.route("/rounds")
def rounds():
    return render_template("rounds.html")


if __name__ == "__main__":
    app.run()
