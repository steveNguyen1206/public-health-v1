from flask import Flask, render_template, send_from_directory, jsonify, request, redirect, url_for
from database import get_all_persons, add_family_person, get_all_families, get_dist_person_num,get_num_persons_of_districts,get_age_groups,get_population,get_household,get_gender,get_occupation,get_num_persons_of_provinces,get_num_persons_of_family,get_num_persons_of_wards

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/api/person/all")
def api_get_all_persons():
    persons = get_all_persons()
    # print(users)
    return jsonify(persons)

# @app.route("/api/family/all")
# def api_get_all_families():
#     families = get_all_families()
#     # print(users)
#     return jsonify(families)

@app.route("/api/ward/num")
def api_get_num_persons_of_wards():
    num_persons_of_wards = get_num_persons_of_wards()
    # print(users)
    return jsonify(num_persons_of_wards)


@app.route("/api/district/num")
def api_get_num_persons_of_districts():
    num_persons_of_districts = get_num_persons_of_districts()
    # print(users)
    return jsonify(num_persons_of_districts)

@app.route("/api/province/num")
def api_get_num_persons_of_provinces():
    num_persons_of_provinces = get_num_persons_of_provinces()
    # print(users)
    return jsonify(num_persons_of_provinces)

@app.route("/api/member/num")
def api_get_num_persons_of_family():
    num_persons_of_family = get_num_persons_of_family()
    # print(users)
    return jsonify(num_persons_of_family)

@app.route("/api/age_groups")
def api_get_all_families():
    age_groups = get_age_groups()
    return jsonify(age_groups)

@app.route("/add-family", methods=['post'])
def add_family_route():
    data=request.form
    print(data)
    # print(data['gender'])
    add_family_person(data)
    return redirect(url_for('api_get_all_persons'))

@app.route("/api/population")
def api_get_population():
    population = get_population()
    return jsonify(population)

@app.route("/api/household")
def api_get_household():
    household = get_household()
    return jsonify(household)

@app.route("/api/gender")
def api_get_gender():
    gender = get_gender()
    return jsonify(gender)

@app.route("/api/occupation")
def api_get_occupation():
    occupation = get_occupation()
    return jsonify(occupation)

@app.route('/survey', methods = ['GET'])
def render_survey():
    if request.method == 'POST':
        return jsonify({'test': 'pass'})
    elif request.method == 'GET':
        return render_template('survey.html')

@app.route('/get-test')
def api_get_dist_person_num():
    args = request.args
    print(args['dist'])
    data = get_dist_person_num(args['dist'])
    return jsonify(data)
    

@app.route('/css/<path:filepath>')
def sendDirCss(filepath):
    return send_from_directory('css/', filepath)

@app.route('/images/<path:filepath>')
def sendDirImgs(filepath):
    return send_from_directory('images/', filepath)

@app.route('/videos/<path:filepath>')
def sendDirVideos(filepath):
    return send_from_directory('videos/', filepath)


@app.route("/survey")
def survey():
    return render_template('survey.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)