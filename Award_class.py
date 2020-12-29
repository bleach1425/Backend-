#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
from Unity_class import unity
Unity = unity()

class awards():
    def __init__(self):
        self.name = "Awards class"
    # input-->account, email, cellphone, unit, job, english
    # output --> currect response(all input give for fontend check)
    #        --> error response( status : error)
    def invite_acount(self, account_, email_, cellphone_, unit_, job_, english_):
        db, cursor = Unity.DB_SET()
        sql = f"SELECT * FROM `test` WHERE `Cellphone` = {cellphone_}"
        data = cursor.execute(sql)
        datetime_ = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if data == 0:
            sql = f"INSERT INTO `test`(`Cellphone`, `account`, `captcha`, `email`, `identity`, `job`, `unit`, `isOnline`, `uid`, `english`, `datetime`) VALUES ('{cellphone_}', '{account_}', 'captcha', '{email_}', 'identity', '{job_}',  '{unit_}', 'False', 'uid', '{english_}', '{datetime_}')"
            data = cursor.execute(sql)
            data_dict = {
                "status": "correct",
                "account": account_,
                "email": email_,
                "cellphone": cellphone_,
                "english": english_,
                "datetime": datetime_
            }
            db.commit()
            return data_dict
        elif data != 0:
            return {"status": "error", "message": "申請的電話已重複"}

    # input--> email, cellphone
    # output --> status if currect response(cellphone correspond user)
    def check(self, cellphone_, name_):
        db, cursor = Unity.DB_SET()
        try:
            sql = f"SELECT * FROM `test` WHERE `Cellphone` = {cellphone_}"
            data = cursor.execute(sql)
            name = data[0][1]
            check_response = data[0]
            if name == name_:
                return {'check_response': check_response}
            else:
                return {"status": "error", "message": "name error"}
        except:
            return {"status": "error", "message": "Not registered"}

    # input --> cellphone, identity, captcha
    # output --> Currect
    def add_identity_code(self, cellphone_, identity_, captcha_):
        db, cursor = Unity.DB_SET()
        # print(cellphone_, identity_)
        sql = f"UPDATE `test` SET `identity`='{identity_}', `captcha`='{captcha_}' WHERE `Cellphone`= '{cellphone_}'"
        # print(sql)
        data = cursor.execute(sql)
        db.commit()
        return {"status": "currect", "message": "Update Currect"}