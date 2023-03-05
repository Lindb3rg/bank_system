from flask import Blueprint, render_template,flash,url_for,jsonify
from datetime import datetime
from flask_security import auth_required,roles_accepted,login_required,current_user, hash_password
from forms import Register_new_user,Edit_new_user
from flask import request, redirect
from model import db,user_datastore,User,Role



admin_BP = Blueprint('admin_BP', __name__)







# @admin_BP.route("/api/<id>")
# def more_transactions(id):
#     transaction_list=[]
#     page = int(request.args.get('page',1))
#     current_transactions = Transaction.query.filter_by(AccountId=id)
#     transactions = current_transactions.order_by(Transaction.Id.desc()).paginate(page=page,per_page=10    )
#     for transaction in transactions.items:
#         t = { "Id": transaction.Id,"Type":transaction.Type, "Operation":transaction.Operation, "Date": transaction.Date, "Amount":transaction.Amount,"NewBalance":transaction.NewBalance }
#         transaction_list.append(t)
#     return jsonify(transaction_list)






@admin_BP.route("/register_user", methods = ["GET","POST"])
@auth_required()
@roles_accepted("Admin")
def register_user_page():
    register_user = Register_new_user()
    if register_user.validate_on_submit():
        user_datastore.create_user(email=register_user.user_email.data, password=hash_password(register_user.password.data),roles=[register_user.user_role.data])
        user_datastore.db.session.commit()
        flash(f"{register_user.user_role.data} user {register_user.user_email.data} added to database")
    return render_template("admin_templates/register_user.html", register_user=register_user)






@admin_BP.route("/edit_user", methods = ["GET","POST"])
@auth_required()
@roles_accepted("Admin")
def edit_user_page():

    id = request.args.get('id')
    edit_user = Edit_new_user()
    edit_user.current_user.data = int(id)

    all_users = User.query.all()
   
    for i in all_users:
        edit_user.user_list.choices.append(i.email)
    if edit_user.validate_on_submit():
        # user = User.query.filter_by(email=edit_user.user_list.data).first()
        user = user_datastore.find_user(email=edit_user.user_list.data)
        if edit_user.user_role.data == "Admin":
            
            role = user_datastore.find_role("Cashier")
            user.roles.remove(role)
            role = user_datastore.find_role("Admin")
            user_datastore.add_role_to_user(user,role)

            

        if edit_user.user_role.data == "Cashier":
            role = user_datastore.find_role("Admin")
            user.roles.remove(role)
            role = user_datastore.find_role("Cashier")
            user_datastore.add_role_to_user(user,role)
            

     

        if edit_user.user_email.data:
            user.email = edit_user.user_email.data
        
        if edit_user.password.data:
            user.password = hash_password(edit_user.password.data)

        
        user_datastore.db.session.commit()
        flash(f"Changes Saved!")
    return render_template("admin_templates/edit_user.html", edit_user=edit_user)




@admin_BP.route("/users")
def list_users():
    current_users = User.query.all()
    return render_template("admin_templates/users.html",current_users=current_users)





@admin_BP.route("/status/<id>", methods=["GET"])
@auth_required()
@roles_accepted("Admin")
def manage_user_status(id):
    user = user_datastore.find_user(id=id)
    status = request.args.get('status')
    
    if status == "true":
        user.active = False
        user_datastore.db.session.commit()
        
        
        return redirect("/users")
    
    if status == "false":
        user.active = True
        user_datastore.db.session.commit()
        return redirect("/users")
    
    





    


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



