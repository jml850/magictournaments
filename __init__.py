from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import SECRET_KEY


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "auth.login"


# Importa los blueprints definidos en los archivos routes
from auth import auth as auth_blueprint
from main import main as main_blueprint

# Registra los blueprints con la aplicación
app.register_blueprint(auth_blueprint)
app.register_blueprint(main_blueprint)


@login_manager.user_loader
def load_user(user_id):
    from models import User  # Ahora, importa User dentro de esta función
    return User.query.get(int(user_id))


