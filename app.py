import chessbits
from flask import Flask, render_template, send_file
app = Flask(__name__, template_folder='./web_view', static_url_path='', static_folder='web_view')

@app.route("/")
def hello():
    a = chessbits.specs('pawn')
    return str(a)

@app.route("/queen/", methods=['GET', 'POST'])
def makeQueen():
    chessbits.output(pieces=['queen'], STL=False, WEB=True)
    return "generated queen"

@app.route("/king/", methods=['GET', 'POST'])
def makeKing():
    chessbits.output(pieces=['king'], STL=False, WEB=True)
    return "generated king"

@app.route("/pawn")
def DownloadPawn():
    return send_file('output/pawn.stl')

@app.route("/web_view")
def view():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
