import flask_jwt.config as config
from flask_jwt.models import Users
from flask import request, jsonify
import jwt
from functools import wraps

def token_required(f):
    """
    To verify the token generated
    """
    @wraps(f)
    def verify_token(*args, **kwargs):
        token = None

        #Token exist
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
           return jsonify({'message':'a valid token is missing'})

        #print('Token =', token)

        try:
            #data = jwt.decode(token, app.config['SECRET_KEY'])
            data = jwt.decode(token, config.as_dict().get('SECRET_KEY'))
            #print('Date =', data)

            current_user = Users.query.filter_by(public_id = data['public_id']).first()
            #print('current_user =', current_user)

        except:
            return jsonify({'message' : 'token is invalid'})

        return f(current_user,*args,**kwargs)
    return verify_token
