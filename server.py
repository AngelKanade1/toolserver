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
    err = 0
    if len(request.get_data()) != 0:
        rare = request.values.get("rare")
        techtype = request.values.get("techtype")
        before = int(request.values.get("before"))
        after = int(request.values.get("after"))
        nowfragment = request.values.get("nowfragment")
        if nowfragment != "":
            nowfragment = int(nowfragment)
        else:
            back_data["data"] = "请填写所有数据"
            err = 1

        if before >= after:
            back_data["data"] = "目标不能比当前数据还小"
            err = 1

        if not err:
            result = func.calcUpgradeCost(rare, techtype, before, after, nowfragment)
            back_data["data"] = "需要" + result[0] + "碎片，" + "共计" + result[1] + "钻石，" + result[2] + "金币。"

    return json.dumps(back_data, ensure_ascii=False)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
