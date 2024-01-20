from flask import  request, Blueprint
import datetime as dt 
from dateutil.relativedelta import relativedelta
from db import  players,  users , report_user
from .jtoken import token_required
from flasgger import swag_from



search_bp = Blueprint("search", __name__)

@search_bp.route("/report" , methods=['PUT'])
@swag_from('main.yaml' , endpoint='search/report')
@token_required
def report(usert): 
    try: 
      content_type = request.headers.get('Content-Type', '').lower()
      if 'application/x-www-form-urlencoded' in content_type:
            name = request.form.get("name")
      elif 'application/json' in content_type:
            user_data = request.get_json()
            name = user_data.get("name")
      f =0 
      for u in users:
         if u["username"] == name :
              f = 1
              break 
      if f==0 :
         return {"message" : "username not found"}, 400
      elif f == 1 :
         report_user(name)
         return {"message" : "user is reported"}, 200
    except : 
         return {"message " :" something went wrong , please try again "} , 404

    

#page 3 , get others by name 
@search_bp.route("/searchbyname" , methods=['POST'])
@swag_from('main.yaml', endpoint='search/searchbyname')
@token_required 
def get(usert):
    for u in users: 
        if (u["username"] == usert):
             date_of_birth = u["birthdate"]
             current_date = dt.datetime.now()
             birthdate = dt.datetime.strptime(date_of_birth, "%d/%m/%Y")
             user_age = relativedelta(current_date, birthdate).years
    
    j=0
    content_type = request.headers.get('Content-Type', '').lower()

    if 'application/x-www-form-urlencoded' in content_type:
            name = request.form.get("name")
    elif 'application/json' in content_type:
            user_data = request.get_json()
            name = user_data.get("name")
    message = ""
    c = 0 
    for i in users:
      if (user_age < 18 ):
            date_of_birth = i["birthdate"]
            current_date = dt.datetime.now()
            birthdate = dt.datetime.strptime(date_of_birth, "%d/%m/%Y")
            age = relativedelta(current_date, birthdate).years
            if(name in i["username"]) and (age < 18 ):
              level = str(players[j]["level"])  
              message +=  " user : " + players[j]["joueur"]+ " level : " + level
              c = 1  
      else :     
          if(name in i["username"]):
              level = str(players[j]["level"])  
              message +=  " user : " + players[j]["joueur"]+ " level : " + level
              c = 1 
      j+=1
    if ( c == 1 ):
      return{"message": message } , 200
    else : 
        return{"message" : "no user found"},400

#page 3 , get others by country
@search_bp.route("/searchbycountry" , methods=['POST']) 
@swag_from('main.yaml', endpoint='search/searchbycountry')
@token_required
def get_c(usert):
    for u in users: 
        if (u["username"] == usert):
             date_of_birth = u["birthdate"]
             current_date = dt.datetime.now()
             birthdate = dt.datetime.strptime(date_of_birth, "%d/%m/%Y")
             user_age = relativedelta(current_date, birthdate).years
    j=0
    content_type = request.headers.get('Content-Type', '').lower()

    if 'application/x-www-form-urlencoded' in content_type:
            country= request.form.get("country")
    elif 'application/json' in content_type:
            user_data = request.get_json()
            country = user_data.get("country")
    message = ""
    c = 0 
    for i in users:
      if (user_age < 18 ):
            date_of_birth = i["birthdate"]
            current_date = dt.datetime.now()
            birthdate = dt.datetime.strptime(date_of_birth, "%d/%m/%Y")
            age = relativedelta(current_date, birthdate).years
            if(i["country"] == country ) and (age < 18 ):
                  level = str(players[j]["level"])  
                  message +=  " user : " + players[j]["joueur"]+ " level : " + level
                  c = 1 
      else : 
            if(i["country"] == country ):
                  level = str(players[j]["level"])  
                  message +=  " user : " + players[j]["joueur"]+ " level : " + level
                  c = 1 
             
      j+=1
    if ( c == 1 ):
      return{"message": message } , 200
    else : 
        return{"message" : "no user found"} , 400
        
#page 3 , get others by age 
@search_bp.route("/searchbyage", methods=['POST']) 
@swag_from('main.yaml', endpoint='search/searchbyage')
@token_required
def get_age(usert):
    for u in users: 
        if u["username"] == usert:
            date_of_birth = u["birthdate"]
            current_date = dt.datetime.now()
            birthdate = dt.datetime.strptime(date_of_birth, "%d/%m/%Y")
            user_age = relativedelta(current_date, birthdate).years
    content_type = request.headers.get('Content-Type', '').lower()
    if 'application/x-www-form-urlencoded' in content_type:
            age= int(request.form.get("age"))
    elif 'application/json' in content_type:
            user_data = request.get_json()
            age = int(user_data.get("age"))
    message = ""
    c = 0 
    j = 0
    for i in users:
        date_of_birth = i["birthdate"]
        current_date = dt.datetime.now()
        birthdate = dt.datetime.strptime(date_of_birth, "%d/%m/%Y")
        age_user = relativedelta(current_date, birthdate).years
        if user_age < 18 : 
            if age == age_user and age < 18:
                 level = str(players[j]["level"])  
                 message += f"user: {players[j]['joueur']}, level: {level}"
                 c = 1 
        else : 
             if age == age_user:
                 level = str(players[j]["level"])  
                 message += f"user: {players[j]['joueur']}, level: {level}"
                 c = 1 
        j += 1
    if c == 1:
        return {"message": message}, 200
    else:
        return {"message": "no user found"}, 404  