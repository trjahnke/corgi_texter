from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from corgiTexter import login_manager
from flask_login import UserMixin, LoginManager, current_user, AnonymousUserMixin
from flask import redirect, url_for, render_template
from corgiTexter.models import User, Post
from corgiTexter.admin_portal.admin_forms import numberOverride
from corgiTexter.twilioBackend import client, factPuller, twilio_number

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.admin_level == 2 or current_user.admin_level == 1:
                return True
            else: 
                return False
        else:
            return False

    @expose('/', methods=['GET', 'POST'])
    def index(self):
        form = numberOverride()

        if form.number.data != None:
            client.messages.create(
                        body=factPuller(),
                        from_=twilio_number,
                        to=form.number.data
                    )

        return self.render('admin/index.html', form=form)
            
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))
    

class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.admin_level == 2:
            return True
        else: 
            return False
            
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))


