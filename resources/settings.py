from flask import  abort,  request, Blueprint
from db import delete_user, players, update_country, update_email, update_number, update_pass ,report ,  users, report_list , restart_progress
from project.templates.code import check_password_strength
from .jtoken import token_required
from flasgger import swag_from
import bcrypt
settings_bp = Blueprint("settings", __name__)

#page 3 , when users want to display their current infos 
@settings_bp.route("/profileinfo", methods=['GET']) 
@swag_from('main.yaml', endpoint='settings/profileinfo')
@token_required
def get_user_info(usert):
   
    try:
         user = None  
         for i in users:
             if i["username"] == usert:
                 user = i
                 break  
         for r in report:
             if r["username"] == usert:
                 reports = r["reports"]
                 break  
            
         if user is not None:
            return {
              
            "username": user["username"],
            "country": user["country"],
            "phonenumber": user["phonenumber"],
            "email": user["email"],
            "birthdate": user["birthdate"] , 
            "reports" :  reports
        }
    except KeyError:
       abort(404, description="User not found")

# page 3, when users want to display their games stats
@settings_bp.route("/stats", methods=['GET'])
@swag_from('main.yaml', endpoint='settings/stats')
@token_required
def get_user_stats(usert):
    player = None
    for i in players:
        if i["joueur"] == usert:
            player = i
            break
    if player is not None:
        user = next((u for u in users if u.get("username") == usert), None)
        sorted_players = sorted(players, key=lambda x: x["level"], reverse=True)
        player_rank = sorted_players.index(player) + 1  
        country_players = [p for p in users if p.get("country") == user["country"]]
        sorted_country_players = sorted(country_players, key=lambda x: next((p["level"] for p in players if x["username"] == p["joueur"]), 0), reverse=True)
        for idx, p in enumerate(sorted_country_players):
            if p["username"] == player["joueur"]:
                country_rank = idx + 1
                break
        if player["games_played"] == 0  : 
            percentage = 0 
        else : 
            percentage = player["games_won"] / player["games_played"]

        return {
            "joueur": player["joueur"],
            "level": player["level"],
            "games_played": player["games_played"],
            "percentage_of_games_won": percentage,
            "overall rank" :  player_rank , 
            "rank in country": country_rank 
            
        }
    else:
        abort(404, description="User not found")


#page 3 , nheb nfasakh rouhi 
@settings_bp.route("/delete", methods=['DELETE'])
@swag_from('main.yaml', endpoint='settings/delete')
@token_required
def delete(usert):
    i=0
    for j in players:
            if j["joueur"] == usert:
                     delete_user(usert)
                     return {"message": "user deleted"}, 200 
            i+=1
    else :
         return{"message": "supression not possible at the moment , try again later "}, 404
     
#page 3 , updati rouhi
@settings_bp.route("/update", methods=['PUT'])
@swag_from('main.yaml', endpoint='settings/update')
@token_required
def update(usert):
    content_type = request.headers.get('Content-Type', '').lower()
    if 'application/x-www-form-urlencoded' in content_type:
        password = request.form.get("password")
        country = request.form.get("country")
        phonenumber = request.form.get("phone_number")
        email = request.form.get("email")
    elif 'application/json' in content_type:
        inp = request.get_json()
        password = inp.get("password")
        country = inp.get("country")
        phonenumber = inp.get("phone_number")
        email = inp.get("email")
   
    for i in users:
      if(i["username"]== usert):
         try:
           c=0
           if (password is not None ):
                password_evaluation = check_password_strength(i["username"], i["email"], i["birthdate"], password)
                if "Strong password" in password_evaluation  :
                     c=1
                     hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                     i["password"] = password
                     update_pass(usert , hashed_password)
                else:
                     return {"message": password_evaluation } , 403
           if (country is not None) :
             c=1
             i["country"] = country 
             update_country(usert , country)
           if (phonenumber is not None) :
             c=1
             i["phonenumber"] = phonenumber
             update_number(usert , phonenumber)
           if (email is not None) :
             c=1
             i["email"] = email 
             update_email(usert, email)
           if (c == 1) :
             return{"message": "account updated succesfully"}, 200 
         except Exception as e:
             print(e)
             return{"message": "an error occured , no changes were made"},400

#reset the accounts stats
@settings_bp.route("/deletestats" , methods=['DELETE'])
@swag_from('main.yaml' , endpoint='/settings/deletestats')   
@token_required
def restart(usert):
    i=0
    for j in players:
            if j["joueur"] == usert:
                     restart_progress(usert)
                     return {"message": "All progress is deleted"}, 200 
            i+=1
    else :
         return{"message": "supression not possible at the moment , try again later "}, 404
      
