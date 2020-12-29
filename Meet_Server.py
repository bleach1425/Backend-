#!/usr/bin/python
# -*- coding: utf-8 -*-
from random import Random
from Unity_class import *
from Award_class import *

Unity = unity()
Award = awards()
app = Unity.FLASK_SET()
db, cursor = Unity.DB_SET()

json_data=""
json_list = []
dict_={"playerDatas":json_list}

account_list=[]
email_list=[]
identity_list=[]
captcha_list=[]

###  網頁端  ###
# 搜尋所有資料確認寄信名單
@app.route('/Award/All_Data', methods=["POST", "GET"])
@cross_origin()
def check_User():
    global db, cursor, columns
    sql = "SELECT * FROM `test`"
    data = cursor.execute(sql)
    data = cursor.fetchall()
    # print(data)
    response = {
        "response":data
    }
    json_response = json.dumps(response)
    # print(json_response)
    return json_response

# 新增使用者
@app.route('/Award/login', methods=['GET', "POST"])
@cross_origin()
def make_account():
    # Get url
    user_data = request.get_json()
    account_ = user_data['name']
    email_ = user_data['email']
    cellphone_ = user_data['cellphone']
    unit_ = user_data['unit']
    job_ = user_data['job']
    english_ = user_data['english']
    add = Award.invite_acount(account_, email_, cellphone_, unit_, job_, english_)
    # print("add",add)
    return add

# 確認使用者申請狀況
@app.route('/Award/check', methods=['GET', "POST"])
@cross_origin()
def check_account():
    user_data = request.get_json()
    cellphone_ = user_data['cellphone']
    name_ = user_data['name']
    check_value = Award.check(cellphone_,name_)
    return check_value

## 更新使用者身分及驗證碼
@app.route('/Award/Add_Data', methods=["POST", "GET"])
@cross_origin()
def add_identity():
    global name_list, email_list, identity_list, captcha_list
    random = Random()
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    captcha_ = ""
    length = len(chars) - 1
    for i in range(7):
        captcha_+=chars[random.randint(0, length)]
    data = request.get_json()
    # Add Data
    cellphone_ = data['cellphone']
    identity_ = data['identity']
    account_ = data['account']
    email_ = data['email']
    unit_ = data['unit']
    job_ = data['job']
    captcha_ = identity_+captcha_
    response = Award.add_identity_code(cellphone_, identity_, account_)

    with open("User_Data.json", mode="w" ,encoding="utf-8") as f:
        User_dict={
            "account":account_list,
            "email":email_list,
            "identity":identity_list,
            "captcha":captcha_list
        }
        User_dict["account"].append(account_)
        User_dict["email"].append(email_)
        User_dict["identity"].append(identity_)
        User_dict['captcha'].append(captcha_)
        User_Info = json.dump(User_dict, f)
        print("save data currect !!")

    return response


###  Unity端  ###
# 取得所有資料刪除已離開的使用者
@app.route('/Award/unity', methods=["POST", "GET"])
@cross_origin()
def unity_sever():
    data = request.get_json()
    cellphone_ = data['Cellphone']
    add = Unity.add_unity_online(cellphone_)
    return add

##  新增使用者視訊ID
@app.route('/Award/unity/set_uid', methods=["POST", "GET"])
@cross_origin()
def unity_first_set():
    # data
    data = request.get_json()
    id_ = data["ID"]
    cellphone_ = data['Cellphone']
    account_ = data['account']
    captcha_ = data['captcha']
    identity_ = data['identity']
    email_ = data['email']
    job_ = data['job']
    unit_ = data['unit']
    # print(id_, cellphone_, account_, captcha_, identity_, email_, job_, unit_)
    uid_ = data['uid']
    isOnline_ = data['isOnline']
    # response
    response = Unity.set_uid(id_, cellphone_, account_, captcha_, identity_, email_, job_, unit_, uid_, isOnline_)
    return response

# ## Unity端請求資料
# @app.route('/unity/content', methods=["POST", "GET"])
# @cross_origin()
# def unity_sever_content():
#     global dict_
#     data = request.get_json()
#     dict_['playerDatas'].append(data)
#     return {"status":"currect"}


# 依照驗證碼給予登入
@app.route('/Award/Captcha', methods=["POST", "GET"])
@cross_origin()
def search_email():
    captcha_ = request.args['captcha']
    global db, cursor, columns
    # part 1
    sql=f"SELECT * FROM `test` WHERE `captcha` = '{captcha_}'"
    data_unm = cursor.execute(sql)
    if data_unm == 0:
        return {'status': "error", "message": "驗證碼錯誤"}
    data = cursor.fetchall()
    Data_list = []
    if data[0][3] == captcha_:
        target = dict(zip(columns, list(data[0])))
        return { "rowUserInfo" : target }

# 確認Unity端上線人數
@app.route('/Award/check_online', methods=["POST", "GET"])
@cross_origin()
def check_online():
    response = Unity.check_unity_online()
    return response

# 更新會議端各項數據
@app.route('/Award/save_message', methods=["POST", "GET"])
@cross_origin()
def save_message():
    data = request.get_json()
    # print(data)
    Agendaindex_ = data['AgendaIndex']
    Subtitleindex_ = data['SubtitleIndex']
    PPTindex_ = data['PPTIndex']
    AgendaPPTIndex_ = data['AgendaPPTIndex']
    Music_ = data['music']
    Speakuid_ = data['Speakuid']
    Speakuidbool_ = data['Speakuidbool']
    Speakaudiouidbool_ = data['Speakaudiouidbool']
    response = Unity.save_message_sql(Agendaindex_, Subtitleindex_, PPTindex_, AgendaPPTIndex_, Music_, Speakuid_, Speakuidbool_, Speakaudiouidbool_)
    # print("response data:", response)
    return response

# 查詢會議各項數據回傳
@app.route('/Award/show_message', methods=["POST", "GET"])
@cross_origin()
def show_message():
    data = Unity.show_message_sql()
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
    gc.collect()