import flask
from flask import request, jsonify, render_template
import auto_run as ar
import random

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = '554133288'

# @app.route('/generate_sign', methods=['POST'])
# def generate_sign():
#     data = request.get_json()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/autoRun', methods=['POST'])
def autoRun():
    data = request.get_json()
    distance_plus = random.randint(0, 200)
    # print(data)
    # result = ar.auto_run_post(data["phone"], data["password"], int(data["run_distance"]), int(data["run_time"]), int(data["school_site"]))
    result = ar.auto_run_post_add_track(data["phone"], data["password"], int(data["run_distance"])+distance_plus, int(data["run_time"]), int(data["school_site"]), data["track"])
    return jsonify(result)


@app.route('/api/getTrack', methods=['POST'])
def send_track():
    distance = request.json.get('distance')
    distance_plus = random.randint(0, 200)
    school_site = request.json.get('school_site')
    # print(int(distance)+distance_plus, school_site)
    tack = ar.genTack(int(distance)+distance_plus,int(school_site))

    # 创建响应对象
    response = jsonify({"track": tack})
    # 添加 CORS 头信息
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response

if __name__ == '__main__':
    app.run(debug=True, port=9680)