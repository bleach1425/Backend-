from flask import Flask, jsonify, request, render_template
from flask_cors import cross_origin
import boto3
from random import Random
from werkzeug.utils import secure_filename
import json
import os
import MySQLdb

# db = MySQLdb.connect(host="127.0.0.1", user = "lili", passwd="lili", db="Meetroom", charset="utf8")
db = MySQLdb.connect(host="127.0.0.1", user = "root", passwd="", db="mysql_test", charset="utf8")

cursor = db.cursor()
db.ping(True)

main_path = os.getcwd()
# dynamodb = boto3.resource('dynamodb',
#                           AWS KEY",
#                           AWS access,
#                           region_name="ap-east-1")
# table = dynamodb.Table('Meet')
# table1 = dynamodb.Table('Meetinfo')




def meet(account_, password_, mail_, name_, cellphone_):
    global db, cursor
    sql = f"SELECT * FROM `Meet` WHERE `account`= '{account_}'"
    data_num = cursor.execute(sql)
    if data_num == 0:
        sql = f"INSERT INTO `Meet`(`name` ,`account`, `password`, `Cellphone`, `email`) VALUES('{name_}' ,'{account_}', '{password_}', '{cellphone_}', '{mail_}')"
        cursor.execute(sql)
        db.commit()
        response = {'account': account_,'password': password_}
        response = json.dumps(response)
        return response
    return {'status': "error" , 'message':"帳號已被註冊" }


def login_meet(account_, password_):
    global db, cursor
    sql = f"SELECT * FROM `Meet` WHERE `account` = '{account_}' "
    data_num = cursor.execute(sql)
    data = cursor.fetchall()
    if data_num == 0:
        return {'status': "error", 'message': "查無此用戶"}
    message = {
        "account": account_,
        "password": password_,
        "name": data[0][6]

    }
    if data_num != 0:
        if data[0][2] == password_:
            return {"status": "correct", "message": message}
        elif data[0][2] != password_:
            return {"status": "error", "message": "帳號或密碼輸入錯誤"}

def id_(id):
    first_word = 0
    second_word = 8
    id_list = []
    id = id.replace("[", "")
    id = id.replace("]", "")
    id = id.replace('"', "")
    for n in range(int(len(id) / 8)):
        try:
            if id[first_word:second_word] != "":
                id_list.append(id[first_word:second_word])
                first_word += 9
                second_word += 9
        except:
            break
    return id_list


def mkdir(path):
    folder = os.path.exists(path)

    if not folder:
        os.makedirs(path)
        print('-----建立成功-----')

    else:
        print(path + '目錄已存在')


#
app = Flask(__name__)


# CORS(app)
@app.route('/', methods=['GET'])
def html():
    return render_template('index.html')



@app.route('/meet/login', methods=['GET'])
@cross_origin()
def check_account():
    account_ = request.args['account']
    password_ = request.args['password']
    final = login_meet(account_, password_)
    return final


@app.route('/meet', methods=['GET', 'POST'])
@cross_origin()
def get_meet_room():
    # print('0')
    data = request.get_json()
    account_ = data['account']
    password_ = data["password"]
    mail_ = data['mail']
    name_ = data['name']
    cellphone_ = data['cellphone']
    # print('1')
    # response = {
    #     'account': account_,
    #     'password': password_
    # }
    response = meet(account_, password_, mail_, name_, cellphone_)
    # print('2')
    return response


@app.route('/file', methods=["POST", "GET"])
@cross_origin()
def get_file():
    ID = request.args['id']
    num = request.args['num']
    # print(num)
    for n in range(int(num)):
        file = request.files.get('file' + str(n))
        file_name = secure_filename(file.filename)
        try:
            file_type = file_name.split('.')[1]
            os.chdir('./picture')
            mkdir(ID)
            file.save(main_path + '/picture/' + ID + '/' + file_name)
            os.chdir(main_path)
        except:
            file_type = file_name
            os.chdir('./picture')
            mkdir(ID)
            file.save(main_path + '/picture/' + ID + '/' + str(n) + "." +file_type)
            os.chdir(main_path)
    return "儲存成功"


@app.route('/meetinfo', methods=["POST"])
@cross_origin()
def sever_info():
    # global dynamodb
    global db, cursor
    a = True
    message = request.get_json()
    account = message["account"]
    password = message["password"]
    message1 = json.dumps(message)
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(8):
        str += chars[random.randint(0, length)]
    captcha = str
    # --------------------------------------------------------------#
    #新增
    sql = f'INSERT INTO `Meetinfo`(`ID`, `captcha`, `Message`, `account`, `Status`) VALUES("ID","{captcha}", "{message}", "{account}", "Status")'
    # print(sql)
    cursor.execute(sql)
    db.commit()
    test = cursor.fetchall()
    # --------------------------------------------------------------#
    #查詢meetid
    sql = f"SELECT * FROM `Meet` WHERE `account` = '{account}'"
    data_num = cursor.execute(sql)
    data = cursor.fetchall()
    # print("data", data)
    meet_id = data[0][3]
    if data_num == 0:
        sql = f"INSERT INTO `Meet`(`ID`, `account`, `password`, `meet_id`) VALUES('ID', '{account}', '{password}', '{captcha}')"
        # print('3')
        cursor.execute(sql)
        db.commit()
        return captcha
    elif data_num != 0:
        try:
            meet_id = meet_id + ',' + captcha
        except:
            meet_id = captcha
        sql = f"UPDATE `Meet` SET `meet_id` = '{meet_id}' WHERE `account` = '{account}'"
        # print('4')
        cursor.execute(sql)
        db.commit()
        return captcha

@app.route('/viewmeet', methods=["GET", "POST"])
@cross_origin()
def get_user_id():
    global db, cursor
    account = request.args['account']
    # print("account", account)
    sql = f"SELECT * FROM `Meet` WHERE `account` = '{account}'"
    data_num = cursor.execute(sql)
    print(data_num)
    data = cursor.fetchall()
    if data[0][3] == None:
        return {'status': "error", 'message': "用戶尚未創建會議"}
    id = data[0][3]
    print(id)
    id_list=id_(id)
    message_list=[]
    # print("1")
    for n in id_list:
        sql = f"SELECT `Message` FROM `Meetinfo` WHERE `captcha` = '{n}'"
        data_num = cursor.execute(sql)
        # print("sql", sql)
        data = cursor.fetchall()
        # print("data_num",data_num)
        # print("data: ",data)
        message = data
        message_list.append(message)
    # print("2")
    response_data={
        'id':id_list,
        "message":message_list
    }
    # print("response_data", response_data)
    json_response_data = json.dumps(response_data)
    # print("json_response_data: ", json_response_data)
    return json_response_data


@app.route('/checkid', methods=["GET"])
@cross_origin()
def check_ID():
    global db, cursor
    ID = request.args['id']
    sql = f"SELECT `Message` FROM `Meetinfo` WHERE `captcha` = '{ID}'"
    data_num = cursor.execute(sql)
    if data_num == 0:
        return {'status':"error", 'message' : "查無此會議空間" }
    data = cursor.fetchall()
    # print("data[0]", data[0][0])
    json_ID_response = json.dumps(data[0][0])
    return json_ID_response



@app.route('/update', methods=["GET"])
@cross_origin()
def update_meetinfo():
    global db, cursor
    message = request.args['message']
    ID = request.args['id']
    account = request.args['account']
    # print("message" ,message, type(message))
    sql = f'UPDATE `Meetinfo` SET `captcha`= "{ID}", `message` = "{message}", `account` = "{account}" WHERE `captcha` = "{ID}"'
    # print(sql)
    cursor.execute(sql)
    db.commit()
    return "OK"

# @app.route('/trytrysee', methods=["GET", "POST"])
# def see():
#     global db, cursor
#     sql = "SELECT * FROM `Meet`"
#     print()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
