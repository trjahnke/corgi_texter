from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from corgiTexter import login_manager
from flask_login import UserMixin, LoginManager, current_user
from flask import redirect, url_for
from corgiTexter.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin == True
        else: 
            return False
            
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))
    

class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin == True
        else: 
            return False
            
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))


