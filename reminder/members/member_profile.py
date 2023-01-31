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

member_profile = Blueprint("member_profile", __name__, static_folder="static", template_folder="templates")

base_url = config('BASE_URL')
current_time = datetime.now(pytz.timezone('Africa/Lusaka'))  
project_enviroment  = config('ENVIROMENT')

@member_profile.route("/show_member", methods=['POST'])
def show_member():

    return "member"