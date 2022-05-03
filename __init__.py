from flask import Flask, redirect, url_for, request
from flask_sqlalchemy import Model, SQLAlchemy
from os import path
from flask_login import LoginManager, current_user  
from flask_admin import Admin 
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
import os.path as op
from flask_admin.menu import MenuLink


db = SQLAlchemy()
DB_NAME = "database.db"



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'


    
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(int(id))
    
    admin= Admin(app)   
    
    
    
    class MyModelView(ModelView):
        column_list = ('id','first_name', 'last_name','password','email', 'address','birthdate')
        column_searchable_list = ['id','first_name', 'last_name', 'email', 'address','birthdate']
        column_filters = ['id','first_name', 'last_name', 'password','email', 'address','birthdate']
        column_editable_list = ['first_name', 'last_name','email', 'address','birthdate']
        edit_template = 'base.html'
        
    class MyModelView2(ModelView):
        column_list = ['user_id', 'id','data','date']
        column_editable_list = ['data']
        column_filters = ['id','user_id','data', 'date']
        column_searchable_list = ['id','user_id','data', 'date']
        

    admin.add_view(MyModelView(User,db.session))
    
    admin.add_view(MyModelView2(Note,db.session))
    
    
    
    admin.add_link(MenuLink(name='Logout', category='', url="/logout"))
    

    
        
    path = op.join(op.dirname(__file__), 'static')
    admin.add_view(FileAdmin(path, '/static/', name='Static Files'))
    

        
        
    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
        