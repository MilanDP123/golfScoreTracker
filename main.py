from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)


def calculateGross(handicap, tee, stableford_points):
    return str(72 + getStrokes(handicap, tee) + (36 - stableford_points))


def getStrokes(handicap, tee):
    # get strokes from database
    return 0


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
        gross = calculateGross(int(handicap), tee, int(stableford_points))

        return render_template("calculate.html",
                               tee=tee,
                               stableford_points=stableford_points,
                               handicap=handicap,
                               gross=gross)

    return render_template("calculate.html")


if __name__ == "__main__":
    app.run(debug=True)
