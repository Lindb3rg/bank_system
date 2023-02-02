from flask_wtf import FlaskForm
from wtforms import Form,BooleanField,StringField,PasswordField,validators,ValidationError
from wtforms.fields import IntegerField, TextAreaField


class Issue_report_form(FlaskForm):
    name = StringField('name', validators=[validators.DataRequired()])
    email = StringField('email', validators=[validators.DataRequired()])
    userid = IntegerField('userid', validators=[validators.DataRequired()])
    textfield = TextAreaField('textfield', validators=[validators.DataRequired()])

    
    
    

    


    