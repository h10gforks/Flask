from . import api
from app import db
from flask import request,jsonify,Response
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User

import json
import redis

@api.route('/message/', methods = ['POST'])
def message():
    if request.method == 'POST':
        myid = request.get_json().get("myid")
        #message list
        conn = redis.StrictRedis(host='redis', decode_responses=True, port=6380, db=10)
        messagelist = eval(conn.get(myid))
        if messagelist == []:
            return jsonify({
                "message":"none"
            }), 200
        else:
            conn.set(myid,str([]))
            return jsonify(messagelist), 200
