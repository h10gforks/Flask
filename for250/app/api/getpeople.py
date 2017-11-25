#coding:utf-8
from . import api
from app import db
from flask import request,jsonify,Response
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User
import json

@api.route('/getpeople/<int:myid>/', methods = ['GET'])
def getpeople(myid):
    if request.method == 'GET':
        users = User.query.all()

        for u in users:
            if u.id == myid:
                users.remove(u)
        
        return Response(json.dumps({
            "people":[{
                "uid":u.id,
                "username":u.username,
                "specialty":u.specialty
                } for u in users]}
        ),mimetype='application/json')
