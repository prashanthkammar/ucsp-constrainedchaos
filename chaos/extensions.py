from flask_login import LoginManager 
from flask_sqlalchemy import SQLAlchemy 
from flask_admin import Admin 
from flask_admin.contrib.sqla import ModelView 

login_manager = LoginManager()
db = SQLAlchemy()
admin = Admin(name='Control Panel')