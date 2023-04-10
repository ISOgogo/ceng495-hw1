from app import (app, mongo_session, mongo_db, session, request)
from modules.auth.schema import *
from flask import render_template, redirect
from models.user.queries import UserQueryOps
from modules.commons import mongo_transaction_with_retry
from pymongo.errors import PyMongoError
from custom_errors import *
from . import auth_bp
from models.user.base import User
from modules.auth.helpers import *

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    result_status = True
    result_msg = 'Authenticated successfully!'
    try:
        auth_register_params = AuthRegisterParams(
            email = request.form.get('email'),
            username = request.form.get('username'),
            password = request.form.get('password')
            )
        new_user = User(email=auth_register_params.email, 
                        username=auth_register_params.username, 
                        password=auth_register_params.password
                        )
        
        user_query_ops = UserQueryOps(mongo_db, mongo_session)
        mongo_transaction_with_retry(lambda: user_query_ops.create(new_user))

    except EmailAlreadyUsed:
        result_status = False
        result_msg = 'This email already registered!'
    except EmptyEmailError:
        result_status = False
        result_msg = 'Email can not be empty!'
    except InvalidEmail:
        result_status = False
        result_msg = 'Email is invalid!'
    except InvalidUsername:
        result_status = False
        result_msg = 'Username must be longer than 3 characters'
    except InvalidPassword:
        result_status = False
        result_msg = 'Password must be longer than 6 character long and contains at least 1 digit & 1 letter!'
    except PyMongoError:
        result_status = False
        result_msg = 'Database connection error. Please try again later!'
    except Exception as e:
        result_status = False
        result_msg = str(e)
    
    if result_status == True:
        session['username'] = new_user.username
        return redirect('/')
    if result_status == False:
        print(result_msg)
        session['result_msg'] = result_msg
        return redirect('/auth')
        

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    result_status = True
    result_msg = 'Authenticated successfully!'
    try:
        auth_login_params = AuthLoginParams(
            username= request.form.get('username'),
            password = request.form.get('password')
            )
        user = validate_and_get_user(auth_login_params, mongo_db, mongo_session)
        session['username'] = user.username
    
    except InvalidUsername:
        result_status = False
        result_msg = 'Username must be longer than 3 characters'
    except UserNotFound:
        result_status=False
        result_msg= 'This username is not registered'
    except InvalidPassword:
        result_status=False
        result_msg = 'Incorrect Password'
    except Exception as e:
        result_status = False
        result_msg = str(e)

    if result_status == True:
        return redirect('/')
    if result_status == False:
        print(result_msg)
        session['result_msg'] = result_msg
        return redirect('/auth')


@auth_bp.route('/auth', methods=['GET'])
def auth_view():
    result_msg = session.pop("result_msg", "")
    return render_template('auth.html', result_msg = result_msg)
