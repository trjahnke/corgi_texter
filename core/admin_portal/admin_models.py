from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from core import login_manager, db
from flask_login import UserMixin, LoginManager, current_user, AnonymousUserMixin
from flask import redirect, url_for, render_template
from core.models import User, Post
from core.admin_portal.admin_forms import numberOverride
from core.twilioBackend import client, factPuller
import os

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.admin_level in [2, 1]
        else:
            return False

    @expose('/', methods=['GET', 'POST'])
    def index(self):
        form = numberOverride()

        if form.number.data != None:
            client.messages.create(
                        body=factPuller(),
                        from_=os.environ['TWILIO_NUMBER'],
                        to=form.number.data
                    )

        return self.render('admin/index.html', form=form)
            
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))
    

class MyModelViewUser(ModelView):
    column_list = ('username', 'email', 'image_file', 'active', 'admin_level', 'id')
    def is_accessible(self):
        return bool(current_user.is_authenticated and current_user.admin_level == 2)

class MyModelViewPost(ModelView):
    column_labels = {'author.username':'Username'}
    column_list = ['fact', 'source', 'date_posted', 'author.username']
    
    def is_accessible(self):
        return bool(current_user.is_authenticated and current_user.admin_level == 2)
            
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))


