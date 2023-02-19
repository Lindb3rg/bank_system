from flask_wtf import FlaskForm
from wtforms import Form,BooleanField,StringField,PasswordField,validators,ValidationError
from wtforms.fields import IntegerField, TextAreaField, EmailField, SelectField, FloatField,DecimalField
from model import Account

def check_for_account(form,field):
    # account = Account.query.filter_by(Id=field.data).first()
    # print(account)
    if Account.query.filter_by(Id=field.data).first() == None:
        raise ValidationError("Customer not existing")
    


def Null_Value(form,field):
    if field.data == None:
        return True

def emailContains(form, field):
    if not field.data.endswith('.se'):
        raise ValidationError('Måste sluta på .se dummer')

class Issue_report_form(FlaskForm):
    name = StringField('name', validators=[validators.DataRequired()])
    email = EmailField('email', validators=[validators.DataRequired(), validators.Email()])
    userid = IntegerField('userid', validators=[validators.DataRequired()])
    textfield = TextAreaField('textfield', validators=[validators.DataRequired()])
    p1 = BooleanField("p1")
    p2 = BooleanField("p2")
    p3 = BooleanField("p3")



class Deposition_form(FlaskForm):
    deposition = DecimalField('deposit', validators=[validators.DataRequired(message="Minimum 1 SEK"), validators.NumberRange(min=1,message="Minimum 1 SEK")])
    type = SelectField("type", choices=["Deposit cash","Salary","Transfer"], validators=[validators.DataRequired(message="Please select an operation!")])
    confirmation = BooleanField("confirmation",validators=[validators.DataRequired(message="Confirmation needed!")])

class Withdrawal_form(FlaskForm):
    withdrawal = DecimalField('withdrawal', validators=[validators.DataRequired(message="Minimum 1 SEK"), validators.NumberRange(min=1,message="Minimum 1 SEK")])
    type = SelectField("type", choices=["Payment","Transfer"], validators=[validators.DataRequired(message="Please select an operation!")])
    confirmation = BooleanField("confirmation",validators=[validators.DataRequired(message="Confirmation needed!")])




class Transfer_form(FlaskForm): 
    amount = DecimalField("amount",validators=[validators.DataRequired(message="Minimum 1 SEK"),validators.NumberRange(min=1,message="Minimum 1 SEK")])
    accounts_to = SelectField("accounts_to", choices=[],validators=[validators.DataRequired(message="Please select an account!")])
    confirmation = BooleanField("confirmation",validators=[validators.DataRequired(message="Confirmation needed!")])

class Transfer_form_external(FlaskForm): 
    account_to = IntegerField("account_to", validators=[validators.DataRequired(),check_for_account])
    amount = DecimalField("amount",validators=[validators.DataRequired(message="Minimum 1 SEK"),validators.NumberRange(min=1,message="Minimum 1 SEK")])
    confirmation = BooleanField("confirmation",validators=[validators.DataRequired(message="Confirmation needed!")])
    


class Edit_customer_form(FlaskForm):
    first_name = StringField("first_name",default=None)
    last_name = StringField("last_name",default=None)
    street_address = StringField("street_address",default=None)
    city = StringField("city",default=None)
    zipcode = IntegerField("zipcode", validators=[validators.optional()],default=None)
    country = SelectField("country", choices=[""],default=None)
    telephone = IntegerField("telephone", validators=[validators.optional()],default=None)
    email = EmailField("email",default=None)
    

# # class Customer(db.Model):
# #     __tablename__= "Customers"
# #     Id = db.Column(db.Integer, primary_key=True)
# #     GivenName = db.Column(db.String(50), unique=False, nullable=False)
# #     Surname = db.Column(db.String(50), unique=False, nullable=False)
# #     Streetaddress = db.Column(db.String(50), unique=False, nullable=False)
# #     City = db.Column(db.String(50), unique=False, nullable=False)
# #     Zipcode = db.Column(db.String(10), unique=False, nullable=False)
# #     Country = db.Column(db.String(30), unique=False, nullable=False)
# #     CountryCode = db.Column(db.String(2), unique=False, nullable=False)
# #     Birthday = db.Column(db.DateTime, unique=False, nullable=False)
# #     NationalId = db.Column(db.String(20), unique=False, nullable=False)
# #     TelephoneCountryCode = db.Column(db.Integer, unique=False, nullable=False)
# #     Telephone = db.Column(db.String(20), unique=False, nullable=False)
# #     EmailAddress = db.Column(db.String(50), unique=False, nullable=False)
    
    

    


    