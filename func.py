import json

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


def calcBuffData(name, atkbuff, defbuff):
    tech_data = getTechDataByLv(name, 1)
    buff_data = {}
    if atkbuff != 0:
        atkbuff = 0.3 + 0.05 * (atkbuff - 1)
    if defbuff != 0:
        defbuff = 0.3 + 0.04 * (defbuff - 1)
    for key in techData.keys():
        if "atk" in key:
            if tech_data[key] * atkbuff == 0:
                continue
            buff_data[key] = tech_data[key] * atkbuff
    buff_data["def"] = tech_data["def"] * defbuff
    return buff_data

def calcGeneralBuffData(name,generals):
    tech_data = getTechDataByLv(name, 1)
    buff_data = {}
    for general in generals:
        for buff in generalData[general]:
            if name not in buff["type"]:
                continue
            for key in buff.keys():
                if "%" in buff[key]:
                    
            
    


def calcTechStatus(name, lv, general, atkbuff, defbuff):
    tech_data = getTechDataByLv(name, lv)
    tech_lv1_data = getTechDataByLv(name, 1)


def typeTransATK(typestr):
    return typestr + "_atk"


def calcDamage(tech, num, buff, etype):
    etype = typeTransATK(etype)
    atk = tech[etype] + getTechDataByLv(tech["name"], 1)[etype] * buff
    damage = atk * num / 500 * 0.825 / 0.099
    return damage


def calcExactDamage(tech, num, buff, etech):
    damage = calcDamage(tech, num, buff, etech["type"])
    return damage * 1000 / etech["def"]


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
    print(before, after)
    for i in range(before, after):
        need_fragment += upgradeCost[rare][i][0]
        need_coin += upgradeCost[rare][i][1]

    return (str(need_fragment), str(need_fragment * idea), str(need_coin))
