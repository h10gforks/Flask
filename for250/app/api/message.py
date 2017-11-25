#coding:utf-8
from . import api
from app import db
from flask import request,jsonify,Response
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User

import json
import redis
import pickle

@api.route('/message/', methods = ['POST'])
def message():
    if request.method == 'POST':
        myid = request.get_json().get("myid")
        #message list
        conn = redis.StrictRedis(host='redis', port=6380, db=10)
        prem = conn.get(myid)
        if prem is not None:
            messagelist = pickle.loads(prem)
            if messagelist == []:
                return jsonify({
                    "message":"none"
                }), 200
            else:
                conn.set(myid,pickle.dumps([]))
                return jsonify({"messages":messagelist}), 200
        else:
            return jsonify({"message":"notfound"}), 404
