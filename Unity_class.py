#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
from flask import Flask, jsonify, request, render_template
from flask_cors import cross_origin
import gc
import json


columns = ["ID", "Cellphone", "account", "captcha", "email", "identity", "job", "unit", "isOnline", "uid"]

class unity():
    def __init__(self):
        self.name = "Unity 專用"


    def FLASK_SET(self):
        app = Flask(__name__)
        return app


    def DB_SET(self):
        db = MySQLdb.connect("127.0.0.1", "lili", "lili", "Award_Data", charset="utf8")
        cursor = db.cursor()
        db.ping(True)
        return db, cursor

    # No input
    # output --> File User_Online.json now nuity online number of people
    def check_unity_online(self):
        with open("User_Online.json", mode="r", encoding="utf-8") as f:
            data = json.load(f)
            response = data["Playlist"]
            return {"playlist": response}


    # input --> cellphone
    # output --> OK
    def add_unity_online(self, cellphone_):
        with open("User_Online.json", mode="r", encoding="utf-8") as f:
            data = json.load(f)
            if len(data["Playlist"]) == 1:
                print('有一人離開會議室')
                if data["Playlist"][0]["Cellphone"] == cellphone_:
                    print(data["Playlist"][0]["account"], " 已離開伺服器")
                    data = None
                with open("User_Online.json", mode="w", encoding="utf-8") as f:
                    json.dump(data, f)
                    return "OK"

            else:
                print('有多人離開會議室')
                for i, n in enumerate(data["Playlist"]):

                    if data["Playlist"][i]["Cellphone"] == cellphone_:
                        print(data["Playlist"][i]["account"], " 已離開伺服器")
                        del data["Playlist"][i]

                    with open("User_Online.json", mode="w", encoding="utf-8") as f:
                        json.dump(data, f)
                return "OK"


    # input --> AgendaIndex, SubtitleIndex, PPTIndex, AgendaPPTIndex ,Music, Speakuid, Speakuidbool
    # output --> OK
    def save_message_sql(self, AgendaIndex_, SubtitleIndex_, PPTIndex_, AgendaPPTIndex_, Music_, Speakuid_, Speakuidbool_,
                         Speakaudiouidbool_):
        db, cursor = self.DB_SET()
        sql = f"UPDATE `content` SET `content` = '{AgendaIndex_}', `Subtitleindex` = '{SubtitleIndex_}', `PPTindex` = '{PPTIndex_}', `AgendaPPTIndex` = '{AgendaPPTIndex_}', `music` = '{Music_}', `Speakuid`= '{Speakuid_}', `Speakuidbool`= '{Speakuidbool_}', `Speakaudiouidbool`='{Speakaudiouidbool_}' WHERE `ID` = '1'"
        # print(sql)
        cursor.execute(sql)
        db.commit()
        return "OK"

    # output --> Search SQL All Data, change to json backto fondend
    def show_message_sql(self):
        db, cursor = self.DB_SET()
        sql = "SELECT * FROM `content`"
        sql_out = cursor.execute(sql)
        data = cursor.fetchall()

        data_dict = {
            "AgendaIndex": data[0][1],
            "SubtitleIndex": data[0][2],
            "PPTIndex": data[0][3],
            "AgendaPPTIndex": data[0][4],
            "music": data[0][5],
            "Speakuid": data[0][6],
            "Speakuidbool": data[0][7],
            "Speakaudiouidbool": data[0][8]
        }
        final = json.dumps(data_dict)
        return final

    # input --> id, cellphone, account, captcha, identity, email, job, unit, uid, isOnline
    # output --> OK
    def set_uid(self,id_, cellphone_, account_, captcha_, identity_, email_, job_, unit_, uid_, isOnline_):
        with open("User_Online.json", mode="r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if len(data["Playlist"]) >= 1 or data["Playlist"] == None:
                    # print("2")
                    New_data = {
                        "ID": id_,
                        "Cellphone": cellphone_,
                        "account": account_,
                        "captcha": captcha_,
                        "identity": identity_,
                        "email": email_,
                        "job": job_,
                        "unit": unit_,
                        "uid": uid_,
                        "isOnline": isOnline_
                    }
                    data["Playlist"].append(New_data)
                    # print(data)
                    with open("User_Online.json", mode="w", encoding="utf-8") as f:
                        json.dump(data, f)
                        return "OK"
            except:
                # print("3")
                data = {
                    "ID": id_,
                    "Cellphone": cellphone_,
                    "account": account_,
                    "captcha": captcha_,
                    "identity": identity_,
                    "email": email_,
                    "job": job_,
                    "unit": unit_,
                    "uid": uid_,
                    "isOnline": isOnline_
                }
                data_list = [data]
                New_data = {"Playlist": data_list}
                print(New_data)
                print(len(New_data))
                with open("User_Online.json", mode="w", encoding="utf-8") as f:
                    json.dump(New_data, f)
                    return "OK"