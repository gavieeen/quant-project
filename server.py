from flask import Flask, render_template

app = Flask(__name__)
 
 
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/<name>")
def welcome(name):
    return render_template("welcome.html", name=name)

@app.route("/home")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run()