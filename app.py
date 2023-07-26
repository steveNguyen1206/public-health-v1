from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import get_all_users, add_user

app = Flask(__name__)

# users = [
#     {'id': 1,
#      'name': "Quach Thi Lan",
#      'age' : 30,
#      'email': 'thilan@email.com'
#      },
#     {'id': 2,
#      'name': "Quach Thi Lan",
#      'age' : 30,
#      'email': 'thilan@email.com'
#      },    
#      {'id': 3,
#      'name': "Quach Thi Lan",
#      'age' : 30,
#      'email': 'thilan@email.com'
#      },    
#      {'id': 4,
#      'name': "Quach Thi Lan",
#      'age' : 30,
#      'email': 'thilan@email.com'
#      },
# ]

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/users")
def get_user():
    users = get_all_users()
    # print(users)
    return render_template('users.html', users=users)

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
    




if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)