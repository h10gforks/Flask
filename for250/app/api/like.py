from . import api
from app import db
from flask import request,jsonify,Response
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User

import json
import redis

@api.route('/like/', methods = ['POST'])
def like():
    if request.method == 'POST':
        myid = request.get_json().get('myid')
        otherid = request.get_json().get('otherid')
         
        conn = redis.StrictRedis(host='localhost', decode_responses=True, port=6379, db=9)
        mylikes = eval(conn.get(myid))
        if otherid not in mylikes:
            mylikes.append(otherid)
        conn.set(myid, str(mylikes))
        
        otherlikes = eval(conn.get(otherid))
        if myid in otherlikes:
            other = User.query.filter_by(id = otherid).first()
            return jsonify({
                "message":"ok",
                "qq":other.qq
            }),200
        else:
            return jsonify({
                "message":"fail"
            }),200
