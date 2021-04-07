from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from flask_jwt import create_app, db
from flask_jwt.models import Users, Authors
from flask_jwt.wrappers import token_required
from flask_jwt.applogger import applogger

app = create_app()

@app.route('/')
def main():
    applogger().logger.info('{ModuleName} - Message = {Message}'.format(ModuleName=__name__
                                                                       ,Message='Starting app in ' + app.config['FLASK_ENV']))
    return 'A Flask API for testing the JWT authentication mechanism'

#New user registration
@app.route('/register',methods=['POST'])
def register_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = Users(
                      public_id = str(uuid.uuid4())
                    , name = data['name']
                    , password = hashed_password
                    , admin = False
                    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message':'registered successfully'})


@app.route('/login',methods=['POST'])
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        applogger().logger.error('{ModuleName} - Error = {Exception}'.format(ModuleName=__name__, Exception='WWW.Authentication - Basic realm: "login required!!"'))
        return make_response('could not verify', 401, {'WWW.Authentication':'Basic realm: "login required!!"'})

    user = Users.query.filter_by(name = auth.username).first()

    if not user:
        # returns 401 if user does not exist
        return make_response(
            'Could not verify'
           , 401
           , {'WWW-Authenticate': 'Basic realm = "User does not exist !!"'}
        )

    if check_password_hash(user.password,auth.password):
        # generates the JWT Token
        token = jwt.encode({'public_id':user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return make_response(jsonify({'token': token}))

    applogger().logger.error('{ModuleName} - Error = {Exception}'.format(ModuleName=__name__,
                                                                         Exception='WWW.Authentication - Basic realm: "Wrong Password !!"'))
    return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "Wrong Password !!"'})


@app.route('/users',methods=['GET'])
@token_required
def get_users(current_user):
    users = Users.query.all()
    result = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name']      = user.name
        user_data['admin']     = user.admin

        result.append(user_data)

    return jsonify({'users':result})


@app.route('/addAuthor',methods=['POST'])
@token_required
def add_author(current_user):
    data = request.get_json()

    new_author = Authors(
        name = data['name']
       ,country = data['country']
       ,book = data['book']
       ,booker_prize = True
       ,user_id = current_user.id
    )
    db.session.add(new_author)
    db.session.commit()

    return jsonify({'message':'a new author was created'})


@app.route('/authors',methods=['GET'])
@token_required
def get_authors(current_user):
    authors = Authors.query.filter_by(user_id=current_user.id).all()
    result = []

    for author in authors:
        author_data = {}
        author_data['id'] = author.id
        author_data['name'] = author.name
        author_data['book'] = author.book
        author_data['country'] = author.country
        author_data['booker_prize'] = author.booker_prize
        author_data['user_id'] = author.user_id
        result.append(author_data)

    return jsonify({'authors': result})


@app.route('/deleteAuthor/<author_id>',methods=['DELETE'])
@token_required
def delete_author(current_user, author_id):
    author = Authors.query.filter(Authors.id==author_id, Authors.user_id==current_user.id).one_or_none()
    if not author:
        return jsonify({'message': 'author does not exist'})
    db.session.delete(author)
    db.session.commit()

    return jsonify({'message':'Author deleted'})

if __name__ == "__main__":
   app.run(debug = True)
