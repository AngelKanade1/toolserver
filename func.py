import json
from decimal import Decimal

with open("techdata.json", "r", encoding="utf-8") as f:
    techData = json.load(f)

with open("generaldata.json", "r", encoding="utf-8") as f:
    generalData = json.load(f)

upgradeCost = {
    "blue": [(10, 5000), (20, 10000), (40, 20000), (60, 30000), (80, 40000),
             (160, 80000), (240, 120000), (280, 140000), (320, 160000),
             (360, 180000), (400, 200000)],
    "purple": [(6, 15000), (12, 30000), (24, 60000), (36, 90000), (48, 120000),
               (66, 160000), (84, 210000),
               (152, 380000), (180, 450000)],
    "orange": [(4, 30000), (8, 60000), (16, 120000), (32, 240000), (48, 360000),
               (84, 630000), (108, 810000)]
}


def getTechRare(name):
    return techData[name]["rare"]


def getTechDataByLv(name, lv):
    tech = techData[name]
    lv -= 1
    tech_lv_data = {
        "name": tech["name"],
        "rare": tech["rare"],
        "hp": tech["hp"][lv],
        "inf_atk": tech["inf_atk"][lv],
        "car_atk": tech["car_atk"][lv],
        "armor_atk": tech["armor_atk"][lv],
        "building_atk": tech["building_atk"][lv],
        "air_atk": tech["air_atk"][lv],
        "boat_atk": tech["boat_atk"][lv],
        "uboat_atk": tech["uboat_atk"][lv],
        "move": tech["move"],
        "atk_range": tech["atk_range"],
        "eye_range": tech["eye_range"],
        "def": tech["def"],
        "food": tech["food"],
        "fuel": tech["fuel"],
        "ammo": tech["ammo"],
        "type": tech["type"]
    }
    return tech_lv_data


def getOriginTechData(name):
    if "(" in name:
        return getTechDataByLv(name[:name.index("(")], 1)
    return getTechDataByLv(name, 1)


def calcBuffData(name, atkbuff, defbuff):
    tech_data = getOriginTechData(name)
    buff_data = {}
    if atkbuff != 0:
        atkbuff = 0.3 + 0.05 * (atkbuff - 1)
    if defbuff != 0:
        defbuff = 0.3 + 0.04 * (defbuff - 1)
    for key in tech_data.keys():
        if "_atk" in key:
            if tech_data[key] * atkbuff == 0:
                continue
            buff_data[key] = tech_data[key] * atkbuff
    buff_data["def"] = tech_data["def"] * defbuff
    return buff_data


def calcGeneralBuffData(name, generals):
    tech_data = getOriginTechData(name)
    buff_data = {
        "add": {},
        "mult": {}
    }
    add_buff_data = {}
    for general in generals:
        for buffkey in generalData[general]:
            buff = generalData[general][buffkey]
            if tech_data["name"] not in buff["type"]:
                continue
            for key in buff.keys():
                if buff[key] == 0 or key == "type":
                    continue
                if "%" in str(buff[key]):
                    if not buff_data["mult"].get(key):
                        buff_data["mult"][key] = 0
                    buff_data["mult"][key] += int(buff[key][:buff[key].index("%")]) / 100
                else:
                    if not buff_data["add"].get(key):
                        buff_data["add"][key] = 0
                    buff_data["add"][key] += buff[key]

    for key in buff_data["mult"].keys():
        add_buff_data[key] = tech_data[key] * buff_data["mult"][key]

    for key in buff_data["add"].keys():
        add_buff_data[key] = tech_data[key] + buff_data["add"][key]

    return add_buff_data


def calcTechStatus(name, lv, general, atkbuff, defbuff):
    tech_data = getTechDataByLv(name, lv)
    result_tech_data = {}
    buff_data = calcBuffData(name, atkbuff, defbuff)
    general_data = calcGeneralBuffData(name, general)
    for key in tech_data.keys():
        result_tech_data[key] = tech_data[key]
        if buff_data.get(key, 0) == 0 and general_data.get(key, 0) == 0:
            continue
        if buff_data.get(key, 0) != 0:
            result_tech_data[key] = float(Decimal(str(result_tech_data[key])) + Decimal(str(buff_data.get(key))))
        if general_data.get(key, 0) != 0:
            result_tech_data[key] = float(Decimal(str(result_tech_data[key])) + Decimal(str(general_data.get(key))))

    return result_tech_data


def typeTransATK(typestr):
    return typestr + "_atk"


def calcDamage(tech, num, etype):
    etype = typeTransATK(etype)
    atk = tech[etype]
    damage = atk * num / 500 * 0.825 / 0.099
    return damage


def calcExactDamage(tech, num, etech):
    damage = calcDamage(tech, num, etech["type"])
    return damage * 1000 / (etech["def"] + 1000)


def calcKillNum(name, lv, general, num, ename, elv, egeneral, enum, ehp, atkbuff, defbuff, deatk):
    tech1 = calcTechStatus(name, lv, general, atkbuff, 0)
    tech2 = calcTechStatus(ename, elv, egeneral, 0, defbuff)
    exact_damage = calcExactDamage(tech1, num, tech2) * 0.01 * (100 - deatk)
    if ehp == 0:
        ehp = tech2["hp"] * enum - exact_damage
    else:
        ehp -= exact_damage
    knum = ehp / tech2["hp"]
    rest_num = 0
    if knum > int(knum):
        rest_num = int(knum) + 1
    else:
        rest_num = int(knum)
    kill_num = enum - rest_num
    return kill_num, ehp


def battleSimulate(unit1, unit2, lv1, lv2, general1, general2, atkbuff1, atkbuff2, defbuff1, defbuff2, num1, num2,
                   hp1, hp2, deatk1, deatk2, battlelog, round):
    kill_num1, hp2 = calcKillNum(unit1, lv1, general1, num1, unit2, lv2, general2, num2, hp2, atkbuff1, defbuff2, deatk2)
    kill_num2, hp1 = calcKillNum(unit2, lv2, general2, num2, unit1, lv1, general1, num1, hp1, atkbuff2, defbuff1, deatk1)
    round += 1
    battlelog += "第%s回合,%s击杀了%s个%s,%s击杀了%s个%s,%s剩余%s,%s剩余%s<br />" % (
        str(round), unit1, str(kill_num1), unit2, unit2, str(kill_num2), unit1, unit1, str(num1 - kill_num2), unit2,
        str(num2 - kill_num1))
    if num1 - kill_num2 <= 0 or num2 - kill_num1 <= 0 or round == 200:
        return battlelog

    return battleSimulate(unit1, unit2, lv1, lv2, general1, general2, atkbuff1, atkbuff2, defbuff1, defbuff2,
                          num1 - kill_num2, num2 - kill_num1, hp1, hp2, battlelog, round)


def calcUpgradeCost(rare, techtype, before, after, nowfragment):
    idea = 0
    if rare == "blue":
        idea = 20
        if techtype == "normal":
            idea = 15
    elif rare == "purple":
        idea = 80
        if techtype == "normal":
            idea = 50
        if techtype == "lock":
            idea = 100

    elif rare == "orange":
        idea = 200
        if techtype == "normal":
            idea = 100
        if techtype == "lock":
            idea = 400

    need_fragment = -1 * nowfragment
    need_coin = 0
    for i in range(before, after):
        need_fragment += upgradeCost[rare][i][0]
        need_coin += upgradeCost[rare][i][1]

    return str(need_fragment), str(need_fragment * idea), str(need_coin)
