from flask import Flask, redirect, url_for, render_template, request
from db import get_strokes

app = Flask(__name__)


def calculateGross(handicap, tee, stableford_points):
    strokes = get_strokes(tee, handicap)
    return str(72 + strokes + (36 - stableford_points))


@app.route("/")
def home():
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


if __name__ == "__main__":
    app.run(debug=True)
