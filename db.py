import mysql.connector

conn = mysql.connector.connect(
    user='root',
    password='root',
    host='127.0.0.1',
    database='gaming_api',
    auth_plugin='mysql_native_password'
)
cursor = conn.cursor() 
def get_db_connection():
    return  conn, cursor

#getting the list of users 
def users_list():
     cursor.execute("SELECT * FROM users;")
     user_results = cursor.fetchall()
     users = []
     for row in user_results:
       user = {
        "username": row[0],
        "password": row[1],
        "country": row[2],  
        "phonenumber": row[3],
        "email": row[4],
        "birthdate": row[5].strftime("%d/%m/%Y") 
    }
       users.append(user)

     return users 
    
#getting the list of players
def players_list():
     cursor.execute("SELECT * FROM players;")
     player_results = cursor.fetchall()
     players = []
     for row in player_results:
          player = {
             "joueur": row[0],
             "level": row[1],
             "games_played": row[2],
             "games_won": row[3]
    }
          players.append(player)
     return players  

#gettinf the report list
def report_list():
     cursor.execute("SELECT * FROM report ;")
     report_results = cursor.fetchall()
     report = []
     for row in report_results:
          item = {
             "username": row[0],
             "reports": row[1]
    }
          report.append(item)
     return report  

#report a user 
def report_user(username):
       cursor.execute("UPDATE report SET reports = reports + %s WHERE username = %s;",(1 , username, ))
       conn.commit()
       users_list()
       players_list()
       report_list()
      
# add a new user/player 
def add_user(username, password, country, phonenumber, email, birthdate):     
       cursor.execute("INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s);",(username, password, country, phonenumber, email, birthdate,))
       cursor.execute("INSERT INTO players VALUES (%s, %s, %s, %s);",(username, 1 , 0 , 0,))
       cursor.execute("INSERT INTO report VALUES(%s ,  %s);" , (username , 0))
       conn.commit()
       #to keep the current lists that are used in the application updated ( real time updates)
       users_list()
       players_list()
       report_list()
     
#delete a user/player
def delete_user(username):
       cursor.execute("DELETE FROM players WHERE username = %s;",(username,))
       cursor.execute("DELETE FROM users WHERE username = %s;",(username,))
       cursor.execute("DELETE FROM report WHERE username = %s;",(username,))
       conn.commit()
       users_list()
       players_list()
       report_list()

#delete a user/player
def restart_progress(username):
       cursor.execute("UPDATE players SET level = %s WHERE username = %s;",(1 , username,  ))
       cursor.execute("UPDATE players SET games_played = %s WHERE username = %s;",(0 , username,  ))
       cursor.execute("UPDATE players SET games_won = %s WHERE username = %s;",(0 , username,  ))
       conn.commit()
       users_list()
       players_list()
     
def update_pass(username , password):
       cursor.execute("UPDATE users SET password = %s WHERE username = %s;",(password , username, ))
       conn.commit()
       users_list()
       players_list()

def update_country(username , country):
       cursor.execute("UPDATE users SET country = %s WHERE username = %s;",( country, username, ))
       conn.commit()
       users_list()
       players_list()

def update_number(username , phone_number):
       cursor.execute("UPDATE users SET phone_number = %s WHERE username = %s;",(phone_number, username,  ))
       conn.commit()
       players_list()
       users_list()
      

def update_email(username , email):
       cursor.execute("UPDATE users SET email = %s WHERE username = %s;",( email, username, ))
       conn.commit()
       users_list()
       players_list()
      
users = users_list()
players = players_list()
report = report_list()
