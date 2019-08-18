from flask_admin import Admin
from core import app, db
from core.admin_portal.admin_models import MyModelViewUser, MyModelViewPost, MyAdminIndexView
from core.models import User, Post
from flask_admin.menu import MenuLink


admin = Admin(app, name='corgiTexter', template_mode='bootstrap3', index_view=MyAdminIndexView())

admin.add_view(MyModelViewUser(User, db.session))
admin.add_view(MyModelViewPost(Post, db.session))
admin.add_link(MenuLink(name='Main Site', url='/'))


app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'