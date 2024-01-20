from flask import Flask
from resources.user import auth_bp
from resources.search import search_bp
from resources.settings import settings_bp
from flasgger import Swagger
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(search_bp, url_prefix='/search')
app.register_blueprint(settings_bp, url_prefix='/settings')

swagger = Swagger(app, template_file="main.yaml")  #http://127.0.0.1:5000/apidocs/#/

if __name__ == "__main__":
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(search_bp, url_prefix='/search')
    app.register_blueprint(settings_bp, url_prefix='/settings')
    app.run(debug=True)

  




