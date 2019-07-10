from flask_wtf import FlaskForm
from wtforms import (BooleanField, PasswordField, StringField, SubmitField,
                     TextAreaField)
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError, URL)


class numberOverride(FlaskForm):
    number = StringField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('Submit')