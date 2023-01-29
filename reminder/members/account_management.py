from flask import *
import pytz, random, json, jwt
import requests
from random import randint
from time import sleep
from decouple import config
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_jwt_extended import (create_access_token, create_refresh_token, get_jwt_identity, jwt_required)
from werkzeug.security import generate_password_hash, check_password_hash
from .. models.membersModel import Member
from .. models.recordModel import Record
from .. function import convert_phone_number, gen_len_code, sendFile_wa_GAPI, sendFile_wa_GAPI_group, send_wa_GreenAPI, sendBtn_GAPI
from datetime import date, datetime, timedelta
from extensions import db

account_management = Blueprint("account_management", __name__, static_folder="static", template_folder="templates")

base_url = config('BASE_URL')
current_time = datetime.now(pytz.timezone('Africa/Lusaka'))  
project_enviroment  = config('ENVIROMENT')

@account_management.route("/activate", methods=['POST'])
def activate():

    _json = request.json

    _platform = _json['platform']
    _wanumber = _json['wanumber']

    # Checking if values has been passed from the client
    if _platform and _wanumber:
        # Check if mobile is already in the database
        is_user_mobile = Member.query.filter_by(wa_number =_wanumber).first()

        if is_user_mobile:
            #Generate OTP
            otp_code = gen_len_code(6, True)

            message = "Your one time password to activate your reminder account is : " + otp_code
            #Send otp code
            wa_resp = send_wa_GreenAPI("260" + _wanumber, message)
            print(wa_resp)
            token = jwt.encode({'public_id': is_user_mobile.memberid, 'exp' : datetime.utcnow() + timedelta(minutes=60)}, config('SECRET_KEY')) 

            #Update the code
            is_user_mobile.code = otp_code
            db.session.commit()



            resp = jsonify({'status': 200,
                            'isError': 'false',
                            'message' : 'SMS sent successfully',
                            'public_id': token}), 200
            return resp


    else:
        resp = jsonify({'status': 400,
                        'isError': 'true',
                        'message' : 'One or more key values are missing, please enter missing values'}), 400
        return resp


@account_management.route("/verify_otp", methods=['POST'])
def verify_otp():

    _json = request.json

    _platform = _json['platform']
    _otp = _json['otp']

    # Checking if values has been passed from the client
    if _platform and _otp:

        # parameter OTP-TOKEN is available
        header_otp = request.headers.get('OTP-TOKEN') 

        otp_value = jwt.decode(header_otp , algorithms='HS256', verify=True, key=config('SECRET_KEY'))

        # Check if user is in the database
        is_user = Member.query.filter_by(memberid = otp_value['public_id']).first()
        
        if is_user:
           
            # Check if mobile is already in the database
            is_otp = Member.query.filter_by(code = _otp).first()

            if is_otp:

                #Update the code
                is_user.is_activated = True
                db.session.commit()

                resp = jsonify({'status': 200,
                            'isError': 'false',
                            'message' : 'Account verified successfully'}), 200
                return resp
            else:

                resp = jsonify({'status': 400,
                            'isError': 'true',
                            'message' : 'OTP not correct'}), 400
                return resp

    else:
        resp = jsonify({'status': 400,
                        'isError': 'true',
                        'message' : 'One or more key values are missing, please enter missing values'}), 400
        return resp


@account_management.route("/reset_password", methods=['POST'])
def reset_password():

    _json = request.json

    _platform = _json['platform']
    _password = _json['password']
    _confirmpassword = _json['confirmpassword']

    # Checking if values has been passed from the client
    if _platform and _password and _confirmpassword: 

        #password validation
        if len(_password) < 8:

            resp = jsonify({'status': 400, 'isError': 'true', 'message' : 'Password must be more than 8 Characters'})
            return resp
            
        elif _password != _confirmpassword:
            resp = jsonify({'status': 400, 'isError': 'true', 'message' : 'Your passwords do not match'})
            return resp  

        else:

            # parameter OTP-TOKEN is available
            header_otp = request.headers.get('OTP-TOKEN') 

            otp_value = jwt.decode(header_otp , algorithms='HS256', verify=True, key=config('SECRET_KEY'))

            # Check if user is in the database
            is_user = Member.query.filter_by(memberid = otp_value['public_id']).first()
            
            if is_user:

                _hashed_password = generate_password_hash(_password)

                #Update the code
                is_user.password = _hashed_password
                db.session.commit()

                resp = jsonify({'status': 200,
                                'isError': 'false',
                                'message' : 'Password added successfully'}), 200
                return resp
            else:
                resp = jsonify({'status': 400,
                                'isError': 'true',
                                'message' : 'User does not exist'}), 400
                return resp

    else:
        resp = jsonify({'status': 400,
                        'isError': 'true',
                        'message' : 'One or more key values are missing, please enter missing values'}), 400
        return resp


@account_management.route("/login" , methods=['GET' ,'POST'])
def login():
    _json = request.json

    _platform = _json['platform']
    _wanumber = _json['wanumber']
    _password = _json['password']
    _confirmpassword = _json['confirmpassword']

     # Checking if values has been passed from the client
    if _platform and _wanumber and _password and _confirmpassword: 

        #password validation
        if len(_password) < 8:

            resp = jsonify({'status': 400, 'isError': 'true', 'message' : 'Password must be more than 8 Characters'})
            return resp
            
        elif _password != _confirmpassword:
            resp = jsonify({'status': 400, 'isError': 'true', 'message' : 'Your passwords do not match'})
            return resp  

        else:
        
          #check if user exists
            is_user_registered = Member.query.filter_by(wa_number = _wanumber).first()
            
            if is_user_registered:

                _id = is_user_registered.memberid
                _wa_number = is_user_registered.wa_number
                password =is_user_registered.password
                _is_number_verfied = is_user_registered.is_activated

                if check_password_hash(password, _password):

                        refresh = create_refresh_token(identity= _id)
                        access = create_access_token(identity= _id)
                        
                        exp_access_timestamp = datetime.now() + timedelta(hours=6)
                        exp_refresh_timestamp = datetime.now() + timedelta(hours=24)

                        return jsonify( {'status': 200,
                                         'isError': 'false',
                                         'message': 'User successfully authenticated.',
                                         'access' : access,
                                         'access _exp' : exp_access_timestamp , 
                                         'refresh': refresh,
                                         'refresh _exp' : exp_refresh_timestamp }), 200
                else:
                        
                    resp = jsonify({'status': 400,
                                    'merchant_message':'true',
                                    'isError': 'true',
                                    'message' : 'Wrong Number/Password please check and try again'}), 200
                    return resp


            
            else:
                #Whatsapp number not registered
                resp = jsonify({'status': 400,
                                'isError': 'true',
                                'message' : 'Number not registered'}), 400
                return resp

    else:
        resp = jsonify({'status': 400,
                        'isError': 'true',
                        'message' : 'One or more key values are missing, please enter missing values'}), 400
        return resp
