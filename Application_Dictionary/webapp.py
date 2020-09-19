from flask import Flask, render_template, request
import json
from difflib import get_close_matches

app = Flask(__name__)
data = json.load(open("data.json"))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods = ['POST'])
def search():
    global word
    if request.method == "POST":
        word = request.form['word']
        word = word.lower()
        if word in data:
            l_list = data[word]
            return render_template("index.html", text1 = "WORD: %s" % word, text2 = "MEANING:", l_list = l_list)
        elif word.title() in data:
            l_list = data[word.title()]
            return render_template("index.html", text1 = "WORD: %s" % word, text2 = "MEANING:", l_list = l_list)
        elif word.upper() in data:
            l_list = data[word.upper()]
            return render_template("index.html", text1 = "WORD: %s" % word, text2 = "MEANING:", l_list = l_list)
        elif len(get_close_matches(word, data.keys(), cutoff = 0.8)) > 0:
            return render_template("index.html", text3 = "Did you mean %s instead? Press Y if yes, or N if no: " % get_close_matches(word, data.keys())[0], btn = "confirmY.html")
        else:
            return render_template("index.html", text3 = "This word doesn't exist. Please check it again!")

@app.route("/confirm-Y/", methods = ['POST', 'GET'])   
def confirmY():
    if request.method == 'POST':
        if request.form.get("Yes") == "Yes":
            l_list = data[get_close_matches(word, data.keys())[0]]
            return render_template("index.html", text1 = "WORD: %s" % get_close_matches(word, data.keys())[0], text2 = "MEANING:", l_list = l_list)
        elif request.form.get("No") == "No":
            return render_template("index.html", text3 = "This word doesn't exist. Please check it again!")
        else:
            return render_template("index.html")
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
