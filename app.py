import chessbits
from flask import Flask, render_template, send_file
app = Flask(__name__, template_folder='./web_view', static_url_path='/web_view')

@app.route("/")
def hello():
    a = chessbits.specs('pawn')
    return str(a)

@app.route("/pawn")
def DownloadPawn():
    return send_file('output/pawn.stl')

@app.route("/view/")
def view():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
