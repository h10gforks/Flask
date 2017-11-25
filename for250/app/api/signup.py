from . import api
from app import db
from flask import request,jsonify,Response
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User

import json
import redis
import pickle

@api.route('/signup/', methods = ['POST'])
def signup():
    if request.method == 'POST':
        username = request.get_json().get('username')
        password = request.get_json().get('password')
        specialty = request.get_json().get('specialty')
        qq = request.get_json().get('qq')
        if not User.query.filter_by(username = username).first():
            user = User(username = username,
                        password = password,
                        specialty = specialty,
                        qq = qq)
            db.session.add(user)
            db.session.commit()
            
            conn = redis.StrictRedis(host='redis', port=6380, db=9)
            alist = []
            conn.set(user.id, pickle.dumps(alist))
            conn2 = redis.StrictRedis(host='redis', port=6380, db=10)
            conn2.set(user.id, pickle.dumps(alist))
 
            return jsonify({
                "uid":user.id
            })
        else:
            return jsonify({
                "message":"fail"
            }),409
