from flask_wtf import FlaskForm
from wtforms import Form,BooleanField,StringField,PasswordField,validators,ValidationError
from wtforms.fields import IntegerField, TextAreaField, EmailField, SelectField, FloatField



class Issue_report_form(FlaskForm):
    name = StringField('name', validators=[validators.DataRequired()])
    email = EmailField('email', validators=[validators.DataRequired(), validators.Email()])
    userid = IntegerField('userid', validators=[validators.DataRequired()])
    textfield = TextAreaField('textfield', validators=[validators.DataRequired()])
    p1 = BooleanField("p1")
    p2 = BooleanField("p2")
    p3 = BooleanField("p3")



class Deposition_form(FlaskForm):
    deposition = FloatField('deposit', validators=[validators.DataRequired(), validators.NumberRange(min=1)])
    type = SelectField("type", choices=["Deposit cash","Salary","Transfer"], validators=[validators.DataRequired()])
    confirmation = BooleanField("confirmation",validators=[validators.DataRequired()])

class Withdrawal_form(FlaskForm):
    withdrawal = FloatField('withdrawal', validators=[validators.DataRequired(), validators.NumberRange(min=1)])
    type = SelectField("type", choices=["Payment","Transfer"], validators=[validators.DataRequired()])
    confirmation = BooleanField("confirmation",validators=[validators.DataRequired()])




class Transfer_form(FlaskForm): 
    amount = FloatField("amount",validators=[validators.DataRequired(),validators.NumberRange(min=1)])
    accounts_to = SelectField("accounts_to", choices=[],validators=[validators.DataRequired()])
    confirmation = BooleanField("confirmation",validators=[validators.DataRequired()])
    



    
    
    

    


    