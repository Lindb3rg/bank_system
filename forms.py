from flask_wtf import FlaskForm
from wtforms import Form,BooleanField,StringField,PasswordField,validators,ValidationError
from wtforms.fields import IntegerField, TextAreaField, EmailField



class Issue_report_form(FlaskForm):
    name = StringField('name', validators=[validators.DataRequired()])
    email = EmailField('email', validators=[validators.DataRequired(), validators.Email()])
    userid = IntegerField('userid', validators=[validators.DataRequired()])
    textfield = TextAreaField('textfield', validators=[validators.DataRequired()])
    p1 = BooleanField("p1")
    p2 = BooleanField("p2")
    p3 = BooleanField("p3")



class Deposition_form(FlaskForm):
    deposition = IntegerField('deposit', validators=[validators.DataRequired(), validators.NumberRange(min=1)])
    confirmation = BooleanField("confirmation",validators=[validators.DataRequired()])
    
    
    

    
    
    

    


    