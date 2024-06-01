from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from pathlib import Path
from flask_wtf.csrf import CSRFProtect # import csrf protection class

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
csrf = CSRFProtect() 

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-do-not-reveal'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///photos.db'
    CWD = Path(os.path.dirname(__file__))
    app.config['UPLOAD_DIR'] = CWD / "uploads"

    db.init_app(app)
    csrf.init_app(app) # initialising global csrf protection

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
