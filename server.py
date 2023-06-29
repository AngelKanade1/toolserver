from flask import Flask, request, render_template
import func
import json

app = Flask(__name__)


@app.route('/test')
def hello_name():
    return 'hello world'


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/upgradecost', methods=['GET', 'POST'])
def upgradeCost():
    back_data = {}
    if len(request.get_data()) != 0:
        rare = request.values.get("rare")
        techtype = request.values.get("techtype")
        before = int(request.values.get("before"))
        after = int(request.values.get("after"))
        nowfragment = int(request.values.get("nowfragment"))
        
        back_data["data"] = func.calcUpgradeCost(rare, techtype, before, after, nowfragment)
        return json.dumps(back_data, ensure_ascii=False)

    return json.dumps(back_data, ensure_ascii=False)


if __name__ == '__main__':
    app.run(debug=True)
