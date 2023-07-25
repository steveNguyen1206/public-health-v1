from flask import Flask, render_template, send_from_directory


app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/css/<path:filepath>')
def sendDirCss(filepath):
    return send_from_directory('css/', filepath)

@app.route('/images/<path:filepath>')
def sendDirImgs(filepath):
    return send_from_directory('images/', filepath)

@app.route('/videos/<path:filepath>')
def sendDirVideos(filepath):
    return send_from_directory('videos/', filepath)

@app.route('/survey')
def sendDirHTML():
    return render_template('survey.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)