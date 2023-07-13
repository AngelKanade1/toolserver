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


@app.route('/costcalc')
def costcalc():
    return render_template("costcalc.html")


@app.route('/search', methods=['GET', 'POST'])
def search():
    with open('techdata.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    if request.method == 'POST':
        units = request.form['unit']
        return render_template('search.html', data=data, units=units)

    return render_template('search.html', data=data)


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


@app.route("/battlecalc")
def battlecalc():
    with open("generaldata.json", 'r', encoding='utf-8') as f:
        generaldata = json.load(f)

    with open('techdata.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    return render_template("battlecalc.html", generaldata=generaldata, data=data)


lv_rule = {
    "red": 7,
    "orange": 7,
    "purple": 9,
    "blue": 11
}


@app.route("/datacompare", methods=['GET', 'POST'])
def datacompare():
    backdata = {}
    if len(request.get_data()) != 0:
        unit1 = request.form['unit1']
        unit2 = request.form['unit2']
        lv1 = int(request.form['tech1lv'])
        lv2 = int(request.form['tech2lv'])
        if lv_rule[func.getTechRare(unit1)] < lv1 or lv_rule[func.getTechRare(unit2)] < lv2:
            return "等级数据异常"
        general1 = request.form.getlist('general1')
        general2 = request.form.getlist('general2')
        atkbuff1 = int(request.form['atkbuff1'])
        defbuff1 = int(request.form['defbuff1'])
        atkbuff2 = int(request.form['atkbuff2'])
        defbuff2 = int(request.form['defbuff2'])
        backdata["data1"] = func.calcTechStatus(unit1, lv1, general1, atkbuff1, defbuff1)
        backdata["data2"] = func.calcTechStatus(unit2, lv2, general2, atkbuff2, defbuff2)

    return backdata


@app.route("/killcalc", methods=['GET', 'POST'])
def killcalc():
    backdata = {}
    if len(request.get_data()) != 0:
        unit1 = request.form['unit1']
        unit2 = request.form['unit2']
        lv1 = int(request.form['tech1lv'])
        lv2 = int(request.form['tech2lv'])
        if lv_rule[func.getTechRare(unit1)] < lv1 or lv_rule[func.getTechRare(unit2)] < lv2:
            return "等级数据异常"
        general1 = request.form.getlist('general1')
        general2 = request.form.getlist('general2')
        atkbuff1 = int(request.form['atkbuff1'])
        defbuff1 = int(request.form['defbuff1'])
        atkbuff2 = int(request.form['atkbuff2'])
        defbuff2 = int(request.form['defbuff2'])
        num1 = int(request.form["num1"])
        num2 = int(request.form["num2"])

        killnum1 = str(round(func.calcKillNum(unit1, lv1, general1, num1, unit2, lv2, general2, atkbuff1, defbuff2), 2))
        killnum2 = str(round(func.calcKillNum(unit2, lv2, general2, num2, unit1, lv1, general1, atkbuff2, defbuff1), 2))
        backdata = "%s一回合可击杀%s个%s,%s一回合可击杀%s个%s" % (unit1, killnum1, unit2, unit2, killnum2, unit1)
    return backdata


@app.route("/battlesimulate", methods=['GET', 'POST'])
def battlesimulate():
    if len(request.get_data()) != 0:
        pass
    return ""


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
