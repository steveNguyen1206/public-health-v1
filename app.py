from flask import Flask, render_template, send_from_directory, jsonify, request, redirect, url_for
from database import get_all_users, add_user

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/api/users")
def api_get_user():
    users = get_all_users()
    # print(users)
    return jsonify(users)


@app.route("/add-user", methods=['post'])
def add_user_route():
    data=request.form
    # print(data['gender'])
    add_user(data)
    return redirect(url_for('get_user'))

@app.route('/survey', methods = ['POST', 'GET'])
def render_survey():
    if request.method == 'POST':
        return jsonify({'test': 'pass'})
    elif request.method == 'GET':
        return render_template('survey.html')
    

@app.route('/css/<path:filepath>')
def sendDirCss(filepath):
    return send_from_directory('css/', filepath)

@app.route('/images/<path:filepath>')
def sendDirImgs(filepath):
    return send_from_directory('images/', filepath)

@app.route('/videos/<path:filepath>')
def sendDirVideos(filepath):
    return send_from_directory('videos/', filepath)



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)