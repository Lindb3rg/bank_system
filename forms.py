from flask_wtf import FlaskForm
from wtforms import Form,BooleanField,StringField,PasswordField,validators,ValidationError
from wtforms.fields import IntegerField, TextAreaField, EmailField, FieldList, FormField, SelectField

def Check_duplicate_account(account_from,account_to):
    if account_from == account_to:
        raise ValidationError("Cannot use the same account")

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

class Withdrawal_form(FlaskForm):
    withdrawal = IntegerField('withdrawal', validators=[validators.DataRequired(), validators.NumberRange(min=1)])
    confirmation = BooleanField("confirmation",validators=[validators.DataRequired()])




class Transfer_form(FlaskForm):
    accounts_from = SelectField("accounts_from", choices=[],validators=[validators.DataRequired()])
    accounts_to = SelectField("accounts_to", choices=[],validators=[validators.DataRequired()])
    amount = IntegerField("amount",validators=[validators.DataRequired()])
    confirmation = BooleanField("confirmation",validators=[validators.DataRequired()])
    



    
    
    

    


    