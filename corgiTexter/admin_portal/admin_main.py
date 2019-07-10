from flask_admin import Admin
from corgiTexter import app,db
from corgiTexter.admin_portal.admin_models import MyModelView, MyAdminIndexView
from corgiTexter.models import User, Post


admin = Admin(app, name='corgiTexter', template_mode='bootstrap3', index_view=MyAdminIndexView())

admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Post, db.session))

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'