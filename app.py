import chessbits
from flask import Flask, render_template
app = Flask(__name__, template_folder='./web_view')

@app.route("/")
def hello():
    a = chessbits.specs('pawn')
    return str(a)

@app.route("/view/")
def view():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
