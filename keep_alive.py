from flask import Flask, render_template, url_for
from threading import Thread

app = Flask('')

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("yatirim.html")

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()