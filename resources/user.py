import bcrypt
from flask import  jsonify, request , Blueprint
import datetime as dt 
from datetime import time 
from dateutil.relativedelta import relativedelta
from db import add_user, players, users ,update_global_lists
from project.templates.code import check_password_strength
import jwt 
from .config import SECRET_KEY
from flasgger import swag_from
from flask_bcrypt import Bcrypt


auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()

#general leaderboard
@auth_bp.route("/leaderboard", methods=['GET'])
@swag_from('main.yaml' , endpoint='auth/leaderboard')
def leaderboard():
  try:    
      message=""
      player_rank = 0 
      sorted_players = sorted(players, key=lambda x: x["level"], reverse=True)
      for player in sorted_players:
           player_rank += 1  
           message +=  str(player_rank) + " " +  player["joueur"]   + " " + str(player["level"])  + "     "
           if player_rank > 9 :
               break 
      return {"message" : message } , 200     
  except Exception as e:
      print(e)
      return {"message" : "something went wrong"} , 400
     

# when i want to sign in 
@auth_bp.route("/signin" , methods=['POST'])
@swag_from('main.yaml', endpoint='auth/signin')
def login():
    content_type = request.headers.get('Content-Type', '').lower()
    if 'application/x-www-form-urlencoded' in content_type:
            username = request.form.get("username")
            password = request.form.get("password")
    elif 'application/json' in content_type:
            user_data = request.get_json()
            username = user_data.get("username")
            password = user_data.get("password")
    f=0
    for u in users: 
        if (u["username"] == username):
             date_of_birth = u["birthdate"]
             current_date = dt.datetime.now()
             birthdate = dt.datetime.strptime(date_of_birth, "%d/%m/%Y") 
             user_age = relativedelta(current_date, birthdate).years
             f= 1 
    if f == 0 :    
        return {"message": "username not found"}, 404
    for user_item in users:
        if user_age >= 18 : 
            if user_item["username"] == username and bcrypt.check_password_hash(user_item["password"], password):
               token = jwt.encode({'user': username, 'exp': dt.datetime.utcnow() + dt.timedelta(minutes=60)}, 
                                  SECRET_KEY ,  algorithm='HS256')
               return jsonify({"message": "welcome " + username, 'token': token}), 200
            elif user_item["username"] == username and not bcrypt.check_password_hash(user_item["password"], password):
               return jsonify({"message": "wrong password"}), 400
        else : 
            current_time = dt.datetime.now().time()
            ten_pm = time(22, 0)  
            ten_am = time (10 ,0)
            if (current_time >= ten_pm) or (current_time <= ten_am):
                return jsonify({"message" : "something is wrong , re-check later"}),403
            else:
                if user_item["username"] == username and  bcrypt.check_password_hash(user_item["password"], password) :
                  token = jwt.encode({'user': username, 'exp': dt.datetime.utcnow() + dt.timedelta(minutes=60)},
                                      SECRET_KEY ,  algorithm='HS256')
                  return jsonify({"message": "welcome " + username, 'token': token}), 200
                elif user_item["username"] == username and not bcrypt.check_password_hash(user_item["password"], password):
                  return jsonify({"message": "wrong password"}), 400
    return {"message": "user not found"}, 404
            
#user sign up  
@auth_bp.route("/signup" , methods=['POST'])
@swag_from('main.yaml', endpoint='auth/signup')
def signup():
    content_type = request.headers.get('Content-Type', '').lower()
    if 'application/x-www-form-urlencoded' in content_type:
         username = request.form.get("username")
         password = request.form.get("password")
         country = request.form.get("country")
         phonenumber = request.form.get("phone_number")
         email = request.form.get("email")
         birthdate = request.form.get("birthdate")
    elif 'application/json' in content_type: 
         user =  request.get_json() 
         username = user.get("username")
         password = user.get("password")
         country = user.get("country")
         phonenumber = user.get("phonenumber")
         email = user.get("email")
         birthdate = user.get("birthdate")
    if username in users : 
        return{"message" : "user already exists"} , 403 
    bd = dt.datetime.strptime(birthdate, "%d/%m/%Y")
    formatted_bd = bd.strftime("%Y-%m-%d")
    password_evaluation = check_password_strength(username, email, birthdate, password)
    if "Strong password" in password_evaluation  :
         try:
             hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
             add_user(username, hashed_password, country, phonenumber, email,formatted_bd)
             update_global_lists()
             return {"message": "user added successfully"}, 200
         except Exception as e:
             print(e)
             return {"message": "user cannot be added"}, 404
    else : 
        return {"message " : password_evaluation } , 400 