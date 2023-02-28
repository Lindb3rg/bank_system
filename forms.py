from flask_wtf import FlaskForm
from wtforms import Form,BooleanField,StringField,validators,ValidationError
from wtforms.fields import IntegerField, TextAreaField, EmailField, SelectField,DecimalField,TelField,DateField
from model import Account, Customer
from datetime import datetime

def validate_national_id(form,field):
    format_to_string = str(form.birthday.data)
    formatted_birthday = format_to_string.replace("-","")
    formatted_national_id = f"{formatted_birthday}-{form.national_id.data}"
    for i in Customer.query.all():
        if i.NationalId == formatted_national_id:
            raise ValidationError("Customer already existing")


def validate_current_amount(form,field):
    if field.id == "deposition":
        if form.deposition.data > 15000:
            raise ValidationError("Deposition limit 15000 SEK")
    if field.id == "amount":
        if form.amount.data > form.current_balance.data:
            raise ValidationError("Not enough funds")

def validate_current_account(form,field):
    form.current_account.data = float(form.current_account.data)
    if form.account_to.data == form.current_account.data:
        raise ValidationError("Cannot transfer to same account")

def validate_negative_numbers(form,field):
    if field.data < 1:
        raise ValidationError("Cannot use negative values. Must be at least 1 SEK")
        

def validate_active_customer(form,field):
    if field.id == "first_name":
        raise ValidationError("Manage not unavailable due to inactive customer")
    if form.is_active.data == False:
        raise ValidationError("Transactions unavailable due to inactive customer")


def check_for_account(form,field):
    if Account.query.filter_by(Id=field.data).first() == None:
        raise ValidationError("Customer not existing")
    


def validate_length(form,field):
    if field.id == "zipcode":
        if len(field.data) > 5:
            raise ValidationError("Zip code must be 5 digits")  
    elif field.id == "national_id":
        field.data = str(field.data)
        if len(field.data) != 4:
            raise ValidationError("Must be 4 digits")  
    elif len(field.data) > 50:
        raise ValidationError("Must be less than 50 characters")

def validate_date(form,field):
    if field.birthdate > datetime.now():
        raise ValidationError("Date not valid after todays date")













class Issue_report_form(FlaskForm):
    name = StringField('name', validators=[validators.DataRequired()])
    email = EmailField('email', validators=[validators.DataRequired(), validators.Email()])
    userid = IntegerField('userid', validators=[validators.DataRequired()])
    textfield = TextAreaField('textfield', validators=[validators.DataRequired()])
    p1 = BooleanField("p1")
    p2 = BooleanField("p2")
    p3 = BooleanField("p3")



class Deposition_form(FlaskForm):
    deposition = DecimalField('deposit', validators=[validate_negative_numbers,validate_current_amount,validate_active_customer])
    type = SelectField("type", choices=["Deposit cash","Salary","Transfer"], validators=[validators.DataRequired(message="Please select an operation!")])
    confirmation = BooleanField("confirmation",validators=[validators.DataRequired(message="Confirmation needed!")])
    is_active = BooleanField("is_active")




class Withdrawal_form(FlaskForm):
    current_balance = DecimalField("current_balance")
    amount = DecimalField('amount', validators=[validate_negative_numbers,validate_current_amount,validate_active_customer])
    is_active = BooleanField("is_active")
    type = SelectField("type", choices=["Payment","Transfer"], validators=[validators.DataRequired(message="Please select an operation!")])
    confirmation = BooleanField("confirmation",validators=[validators.DataRequired(message="Confirmation needed!")])




class Transfer_form_internal(FlaskForm): 
    current_balance = DecimalField("current_balance")
    amount = DecimalField("amount",validators=[validate_negative_numbers,validate_current_amount,validate_active_customer])
    accounts_to = SelectField("accounts_to", choices=[],validators=[validators.DataRequired(message="Please select an account!")])
    confirmation = BooleanField("confirmation",validators=[validators.DataRequired(message="Confirmation needed!")])
    is_active = BooleanField("is_active")



class Transfer_form_external(FlaskForm):
    current_account = IntegerField("current_account")
    current_balance = DecimalField("current_balance")
    account_to = IntegerField("account_to", validators=[validators.DataRequired(),check_for_account])
    amount = DecimalField("amount",validators=[validate_negative_numbers,validate_current_amount,validate_active_customer,validate_current_account])
    confirmation = BooleanField("confirmation",validators=[validators.DataRequired(message="Confirmation needed!")])
    is_active = BooleanField("is_active")


class Edit_customer_form(FlaskForm):
    first_name = StringField("first_name",default=None, validators=[validate_active_customer])
    last_name = StringField("last_name",default=None)
    street_address = StringField("street_address",default=None)
    city = StringField("city",default=None)
    zipcode = IntegerField("zipcode", validators=[validators.optional()],default=None)
    country = SelectField("country", choices=[""],default=None)
    telephone = IntegerField("telephone", validators=[validators.optional()],default=None)
    email = EmailField("email",default=None)
    is_active = BooleanField("is_active")
    


class Register_customer_form(FlaskForm):
    first_name = StringField("first_name",validators=[validators.DataRequired(message="*required field*"),validate_length])
    last_name = StringField("last_name",validators=[validators.DataRequired(message="*required field*"),validate_length])
    street_address = StringField("street_address",validators=[validators.DataRequired(message="*required field*"),validate_length])
    city = StringField("city",validators=[validators.DataRequired(message="*required field*"),validate_length])
    zipcode = StringField("zipcode", validators=[validators.DataRequired(message="*required field*"),validate_length])
    country = SelectField("country", choices=[""],default=None)
    birthday = DateField("birthday", validators=[validators.DataRequired()])
    national_id = IntegerField("national_id", validators=[validators.DataRequired(message="*required field*"), validate_length,validate_national_id])
    telephone = TelField("telephone", validators=[validators.DataRequired(message="*required field*")])
    email = EmailField("email",validators=[validators.DataRequired(message="*required field*"),validators.Email()])
    confirmation = BooleanField("confirmation",validators=[validators.DataRequired(message="*required field*")])



