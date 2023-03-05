from flask import Blueprint, render_template,flash,url_for,jsonify
from datetime import datetime
from flask_security import auth_required,roles_accepted,login_required,current_user, hash_password

from flask import request, redirect
from model import db,user_datastore,Customer



api_BP = Blueprint('api_BP', __name__)







@api_BP.route("/api/<id>")
def customer_api(id):
    customer_data=[]
    current_customer = Customer.query.filter_by(Id=id)
    
    for data in current_customer:
        t = { "id": data.Id,
             "first_name":data.GivenName,
             "last_name":data.Surname,
             "street_address": data.Streetaddress,
             "city":data.City,
             "zipcode":data.Zipcode,
             "country":data.Country,
             "country_code":data.CountryCode,
             "birthday":data.Birthday,
             "national_id":data.NationalId,
             "telephone_country_code":data.TelephoneCountryCode,
             "telephone":data.Telephone,
             "email_address":data.EmailAddress,
             "active":data.Active,
            
            }
        customer_data.append(t)
        for account in data.Accounts:
            a = {"account_id":account.Id,
                 "account_type":account.AccountType,
                 "created":account.Created,
                 "balance":account.Balance,
                 "customer_id":account.CustomerId
                 }
            customer_data.append(a)

        
        
    return jsonify(customer_data)

#   Id = db.Column(db.Integer, primary_key=True)
#     AccountType = db.Column(db.String(10), unique=False, nullable=False)
#     Created = db.Column(db.DateTime, unique=False, nullable=False)
#     Balance = db.Column(db.Float, unique=False, nullable=False)
#     Transactions = db.relationship('Transaction', backref='Account',
#      lazy=True)
#     CustomerId = db.Column(db.Integer, db.ForeignKey('Customers.Id'), nullable=False)









# @admin_BP.route("/deposit/<id>", methods = ["GET","POST"])

# @auth_required()
# @roles_accepted("Admin","Cashier")
# def deposit(id):
#     id = int(id)
#     account = Account.query.filter_by(Id=id).first()
#     new_deposit = Deposition_form()
#     is_active = Customer.query.filter_by(Id=account.CustomerId).first()
#     new_deposit.is_active.data = is_active.Active
#     if new_deposit.validate_on_submit():
#         account = Account.query.filter_by(Id=id)
#         deposit = Transaction()
#         deposit.AccountId = id
#         deposit.Type = "Debit"
#         deposit.Operation = new_deposit.type.data
#         deposit.Date = datetime.now()
#         deposit.Amount = new_deposit.deposition.data
#         new_deposit.deposition.data = float(new_deposit.deposition.data)

#         for i in account:
#             deposit.NewBalance = i.Balance + new_deposit.deposition.data
#             i.Balance += new_deposit.deposition.data
#             customer = str(i.CustomerId)
        
#         db.session.add(deposit)
#         db.session.commit()


#         flash("Deposition done!")
#         return redirect("/customer/" + str(customer))
    
#     return render_template("account_templates/deposit.html", new_deposit=new_deposit)





# @admin_BP.route("/withdraw/<id>", methods = ["GET","POST"])
# @auth_required()
# @roles_accepted("Admin","Cashier")

# def withdraw(id):
#     id = int(id)
#     new_withdrawal = Withdrawal_form()
#     account = Account.query.filter_by(Id=id).first()
#     new_withdrawal.current_balance.data = account.Balance
#     is_active = Customer.query.filter_by(Id=account.CustomerId).first()
#     new_withdrawal.is_active.data = is_active.Active
#     customer = account.CustomerId
#     if new_withdrawal.validate_on_submit():
        

#         withdraw = Transaction()
#         withdraw.AccountId = id
#         withdraw.Type = "Credit"
#         withdraw.Operation = new_withdrawal.type.data
#         withdraw.Date = datetime.now()
#         withdraw.Amount = new_withdrawal.amount.data
#         new_withdrawal.amount.data = float(new_withdrawal.amount.data)
#         withdraw.NewBalance = account.Balance - new_withdrawal.amount.data
#         account.Balance = account.Balance - new_withdrawal.amount.data
#         db.session.add(withdraw)
#         db.session.commit()
#         flash("Withdrawal done!")
#         return redirect("/customer/" + str(customer))


#     return render_template("account_templates/withdraw.html", new_withdrawal=new_withdrawal)








# @admin_BP.route("/internal/<customer_id>/<account_from>", methods = ["GET","POST"])
# @auth_required()
# @roles_accepted("Admin","Cashier")

# def transfer(customer_id,account_from):
#     customer_id = customer_id
#     account_from = int(account_from)
#     current_account = Account.query.filter_by(Id=account_from).first()
#     current_balance = current_account.Balance
#     customer_accounts = Customer.query.filter_by(Id=customer_id)
#     check_active = Customer.query.filter_by(Id=customer_id).first()
#     new_transfer = Transfer_form_internal()
#     new_transfer.current_balance.data = current_balance
#     new_transfer.is_active.data = check_active.Active
    

#     for i in customer_accounts:
#         if i.Accounts:
#             for account in i.Accounts:
#                 if account.Id == account_from:
#                     continue
#                 else:
#                     new_transfer.accounts_to.choices.append(account.Id)
        

#     if new_transfer.validate_on_submit():
        
#         withdraw = Transaction()
#         withdraw.AccountId = account_from
#         withdraw.Type = "Credit"
#         withdraw.Operation = "Transfer"
#         withdraw.Date = datetime.now()
#         withdraw.Amount = new_transfer.amount.data
#         new_transfer.amount.data = float(new_transfer.amount.data)

#         for i in Account.query.filter_by(Id=account_from):
#             withdraw.NewBalance = i.Balance - new_transfer.amount.data
#             i.Balance -= new_transfer.amount.data
        
#         db.session.add(withdraw)
#         db.session.commit()


#         deposit = Transaction()
#         deposit.AccountId = new_transfer.accounts_to.data
#         deposit.Type = "Debit"
#         deposit.Operation = "Transfer"
#         deposit.Date = datetime.now()
#         deposit.Amount = new_transfer.amount.data
#         for i in Account.query.filter_by(Id=new_transfer.accounts_to.data):
#             deposit.NewBalance = i.Balance + new_transfer.amount.data
#             i.Balance += new_transfer.amount.data
        
#         db.session.add(deposit)
#         db.session.commit()

#         flash("Transfer done!")
#         return redirect("/customer/" + customer_id)
    
#     return render_template("account_templates/internal_transfer.html", account_from = account_from, new_transfer=new_transfer,customer_accounts=customer_accounts)







# @admin_BP.route("/external/<account_from>", methods = ["GET","POST"])
# @auth_required()
# @roles_accepted("Admin","Cashier")
# def external_transfer(account_from):
#     current_account = Account.query.filter_by(Id=account_from).first()
#     current_balance = current_account.Balance
#     check_active = Customer.query.filter_by(Id=current_account.CustomerId).first()
#     new_transfer = Transfer_form_external()
#     new_transfer.current_account.data = account_from
#     new_transfer.current_balance.data = current_balance
#     new_transfer.is_active.data = check_active.Active
#     new_transfer.current_balance.data = current_account.Balance

#     if new_transfer.validate_on_submit():

#         current_account = Account.query.filter_by(Id=account_from).first()
#         customer = str(current_account.CustomerId)

#         external_account = Account.query.filter_by(Id=new_transfer.account_to.data).first()
        
#         transaction_from = Transaction()
#         transaction_from.AccountId = account_from
#         transaction_from.Type = "Credit"
#         transaction_from.Operation = "Transfer"
#         transaction_from.Date = datetime.now()
#         transaction_from.Amount = new_transfer.amount.data
#         new_transfer.amount.data = float(new_transfer.amount.data)
#         transaction_from.NewBalance = current_account.Balance - new_transfer.amount.data

#         transaction_to = Transaction()
#         transaction_to.AccountId = new_transfer.account_to.data
#         transaction_to.Type = "Debit"
#         transaction_to.Date = datetime.now()
#         transaction_to.Operation = "Transfer"
#         transaction_to.Amount = new_transfer.amount.data
#         new_transfer.amount.data = float(new_transfer.amount.data)
#         transaction_to.NewBalance = external_account.Balance - new_transfer.amount.data

#         current_account.Balance -= new_transfer.amount.data
#         external_account.Balance += new_transfer.amount.data

#         db.session.add(transaction_from)
#         db.session.add(transaction_to)
#         db.session.commit()
#         flash("Transfer done!")
#         return redirect("/customer/" + str(customer))
    
#     return render_template("account_templates/external_transfer.html", account_from = account_from, new_transfer=new_transfer)



