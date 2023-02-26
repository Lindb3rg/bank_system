from flask import Flask, render_template, request,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from model import Customer,Account,Transaction
from sqlalchemy import func
from flask_security import roles_accepted, auth_required, logout_user
import os
from model import db, seedData
from forms import Issue_report_form,Deposition_form, Withdrawal_form, Transfer_form_internal, Transfer_form_external, Edit_customer_form,Register_customer_form
import datetime





app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:my-secret-pw@localhost/Bank'
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-123asdasfasdf')
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", '851453681323861735056780167285096341234')
app.config["REMEMBER_COOKIE_SAMESITE"] = "strict"
app.config["SESSION_COOKIE_SAMESITE"] = "strict"


db.app = app
db.init_app(app)
migrate = Migrate(app,db)
 



@app.route("/")
@auth_required()
@roles_accepted("Admin","Cashier")
def startpage():
    total_customers = len(Customer.query.all())
    total_accounts = len(Account.query.all())
    total_balance = Account.query.with_entities(func.sum(Account.Balance).label('total')).first().total
    rounded_total_balance = round(total_balance, 2)

    
    return render_template("start_page.html", total_customers=total_customers,total_accounts=total_accounts,rounded_total_balance=rounded_total_balance)




@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")



@app.route("/messages")
@auth_required()
@roles_accepted("Admin","Cashier")
def messages():
    
    return render_template("messages.html")





    



@app.route("/customers")
@auth_required()
@roles_accepted("Admin","Cashier")

def customerspage():
    sortColumn = request.args.get('sortColumn', 'namn')
    sortOrder = request.args.get('sortOrder', 'asc')
    page = int(request.args.get('page', 1))
    searchWord = request.args.get('q','')

    listOfCustomers = Customer.query

    #sökning i databas
    listOfCustomers = listOfCustomers.filter(
        Customer.GivenName.like('%' + searchWord + '%') |
        Customer.Country.like('%' + searchWord + '%') |    
        Customer.City.like('%' + searchWord + '%' ))
        

    if sortColumn == "namn":
        if sortOrder == "asc":
            listOfCustomers = listOfCustomers.order_by(Customer.GivenName.asc())
        else:
            listOfCustomers = listOfCustomers.order_by(Customer.GivenName.desc())
    elif sortColumn == "city":
        if sortOrder == "asc":
            listOfCustomers = listOfCustomers.order_by(Customer.City.asc())
        else:
            listOfCustomers = listOfCustomers.order_by(Customer.City.desc())
    elif sortColumn == "country":
        if sortOrder == "asc":
            listOfCustomers = listOfCustomers.order_by(Customer.Country.asc())
        else:
            listOfCustomers = listOfCustomers.order_by(Customer.Country.desc())

    paginationObject = listOfCustomers.paginate(page=page,per_page=20,error_out=False )
    return render_template("customers.html", 
                    listOfCustomers=paginationObject.items, 
                    activePage="customersPage",
                    page=page,
                    sortColumn=sortColumn,
                    sortOrder=sortOrder,
                    has_next = paginationObject.has_next,
                    has_prev = paginationObject.has_prev,
                    pages=paginationObject.pages,
                    q = searchWord)




@app.route("/customer/<id>")
# @auth_required()
@roles_accepted("Admin","Cashier")

def customer_page(id):
    customer = Customer.query.filter_by(Id=id).first()
    accounts = Account.query.filter_by(CustomerId=id)
    total = 0
    for account in accounts:
        total += account.Balance
    


    return render_template("customer.html", customer=customer, accounts=accounts,total=total)







@app.route("/account/<customer>/<id>")
@auth_required()
@roles_accepted("Admin","Cashier")
def account_page(customer,id):
    id = int(id)
    customer = customer
    account = Account.query.filter_by(Id=id).first()
    current_transactions = Transaction.query.filter_by(AccountId=id)
    current_transactions = current_transactions.order_by(Transaction.Id.desc())
    
    

    return render_template("account.html", id=id, customer = customer, account=account, current_transactions=current_transactions)





### DEPOSIT ### Deposit cash, Salary, Transfer

@app.route("/deposit/<id>", methods = ["GET","POST"])

def deposit(id):
    id = int(id)
    account = Account.query.filter_by(Id=id).first()
    new_deposit = Deposition_form()
    is_active = Customer.query.filter_by(Id=account.CustomerId).first()
    new_deposit.is_active.data = is_active.Active
    if new_deposit.validate_on_submit():
        account = Account.query.filter_by(Id=id)
        deposit = Transaction()
        deposit.AccountId = id
        deposit.Type = "Debit"
        deposit.Operation = new_deposit.type.data
        deposit.Date = datetime.datetime.now()
        deposit.Amount = new_deposit.deposition.data
        new_deposit.deposition.data = float(new_deposit.deposition.data)

        for i in account:
            deposit.NewBalance = i.Balance + new_deposit.deposition.data
            i.Balance += new_deposit.deposition.data
            customer = str(i.CustomerId)
        
        db.session.add(deposit)
        db.session.commit()


        flash("Deposition done!")
        return redirect("/customer/" + customer)


    return render_template("deposit.html", new_deposit=new_deposit)









@app.route("/withdraw/<id>", methods = ["GET","POST"])

def withdraw(id):
    id = int(id)
    new_withdrawal = Withdrawal_form()
    account = Account.query.filter_by(Id=id).first()
    new_withdrawal.current_balance.data = account.Balance
    is_active = Customer.query.filter_by(Id=account.CustomerId).first()
    new_withdrawal.is_active.data = is_active.Active
    customer = account.CustomerId
    if new_withdrawal.validate_on_submit():
        

        withdraw = Transaction()
        withdraw.AccountId = id
        withdraw.Type = "Credit"
        withdraw.Operation = new_withdrawal.type.data
        withdraw.Date = datetime.datetime.now()
        withdraw.Amount = new_withdrawal.amount.data
        new_withdrawal.amount.data = float(new_withdrawal.amount.data)
        withdraw.NewBalance = account.Balance - new_withdrawal.amount.data
        account.Balance = account.Balance - new_withdrawal.amount.data
        db.session.add(withdraw)
        db.session.commit()
        flash("Withdrawal done!")
        return redirect("/customer/" + str(customer))


    return render_template("withdraw.html", new_withdrawal=new_withdrawal)


@app.route("/withdrawal-confirmation")
def withdrawal_confirmation():
    return render_template("/withdrawal_confirmation.html")










### Internal TRANSFER ###

@app.route("/internal/<customer_id>/<account_from>", methods = ["GET","POST"])

def transfer(customer_id,account_from):
    customer_id = customer_id
    account_from = int(account_from)
    current_account = Account.query.filter_by(Id=account_from).first()
    current_balance = current_account.Balance
    customer_accounts = Customer.query.filter_by(Id=customer_id)
    check_active = Customer.query.filter_by(Id=customer_id).first()
    new_transfer = Transfer_form_internal()
    new_transfer.current_balance.data = current_balance
    new_transfer.is_active.data = check_active.Active
    

    for i in customer_accounts:
        if i.Accounts:
            for account in i.Accounts:
                if account.Id == account_from:
                    continue
                else:
                    new_transfer.accounts_to.choices.append(account.Id)
        

    if new_transfer.validate_on_submit():
        
        withdraw = Transaction()
        withdraw.AccountId = account_from
        withdraw.Type = "Credit"
        withdraw.Operation = "Transfer"
        withdraw.Date = datetime.datetime.now()
        withdraw.Amount = new_transfer.amount.data
        new_transfer.amount.data = float(new_transfer.amount.data)

        for i in Account.query.filter_by(Id=account_from):
            withdraw.NewBalance = i.Balance - new_transfer.amount.data
            i.Balance -= new_transfer.amount.data
        
        db.session.add(withdraw)
        db.session.commit()


        deposit = Transaction()
        deposit.AccountId = new_transfer.accounts_to.data
        deposit.Type = "Debit"
        deposit.Operation = "Transfer"
        deposit.Date = datetime.datetime.now()
        deposit.Amount = new_transfer.amount.data
        for i in Account.query.filter_by(Id=new_transfer.accounts_to.data):
            deposit.NewBalance = i.Balance + new_transfer.amount.data
            i.Balance += new_transfer.amount.data
        
        db.session.add(deposit)
        db.session.commit()

        flash("Transfer done!")
        return redirect("/customer/" + customer_id)
    
    return render_template("internal_transfer.html", account_from = account_from, new_transfer=new_transfer,customer_accounts=customer_accounts)

















### External TRANSFER ###

@app.route("/external/<account_from>", methods = ["GET","POST"])
def external_transfer(account_from):
    current_account = Account.query.filter_by(Id=account_from).first()
    current_balance = current_account.Balance
    check_active = Customer.query.filter_by(Id=current_account.CustomerId).first()
    new_transfer = Transfer_form_internal()
    new_transfer.current_balance.data = current_balance
    new_transfer.is_active.data = check_active.Active

    new_transfer = Transfer_form_external()
    new_transfer.current_balance.data = current_account.Balance

    if new_transfer.validate_on_submit():

        current_account = Account.query.filter_by(Id=account_from).first()
        customer = str(current_account.CustomerId)

        external_account = Account.query.filter_by(Id=new_transfer.account_to.data).first()
        
        transaction_from = Transaction()
        transaction_from.AccountId = account_from
        transaction_from.Type = "Credit"
        transaction_from.Operation = "Transfer"
        transaction_from.Date = datetime.datetime.now()
        transaction_from.Amount = new_transfer.amount.data
        new_transfer.amount.data = float(new_transfer.amount.data)
        transaction_from.NewBalance = current_account.Balance - new_transfer.amount.data

        transaction_to = Transaction()
        transaction_to.AccountId = new_transfer.account_to.data
        transaction_to.Type = "Debit"
        transaction_to.Date = datetime.datetime.now()
        transaction_to.Operation = "Transfer"
        transaction_to.Amount = new_transfer.amount.data
        new_transfer.amount.data = float(new_transfer.amount.data)
        transaction_to.NewBalance = external_account.Balance - new_transfer.amount.data

        current_account.Balance -= new_transfer.amount.data
        external_account.Balance += new_transfer.amount.data

        db.session.add(transaction_from)
        db.session.add(transaction_to)
        db.session.commit()
        flash("Withdrawal done!")
        return redirect("/customer/" + str(customer))
    
    return render_template("external_transfer.html", account_from = account_from, new_transfer=new_transfer)


    
    



### REPORT ###

@app.route("/report-form", methods = ["GET","POST"])

def report_issue():
    form = Issue_report_form()
    if form.validate_on_submit():
        # todays_date = datetime.now()
        # time_date = todays_date.strftime("%Y-%m-%d %H:%M:%S")
        

        return redirect("/report-confirmation?name=" + form.name.data)

    return render_template("/issue_report.html", form=form)


def Change_activity(id):
    customer = Customer.query.filter_by(Id=id)
    customer.Active = False
    db.session.commit()


@app.route("/report-confirmation")
def report_confirmation():
    # user_name = request.args.get("name", " ")
    return render_template("/report_confirmation.html")


# REGISTER CUSTOMER

@app.route("/register", methods = ["GET","POST"])
@auth_required()
@roles_accepted("Admin","Cashier")
def register_customer():
    form = Register_customer_form()
    for i in Customer.query.all():
        if i.Country in form.country.choices:
            break
        form.country.choices.append(i.Country)

   
    if form.validate_on_submit():
        new_customer = Customer()
        new_customer.GivenName = form.first_name.data
        new_customer.Surname = form.last_name.data
        new_customer.Streetaddress = form.street_address.data
        new_customer.City = form.city.data
        new_customer.Zipcode = form.zipcode.data
        new_customer.Country = form.country.data
        new_customer.CountryCode = "US"
        new_customer.Birthday = form.birthday.data
        format_to_string = str(form.birthday.data)
        formatted_birthday = format_to_string.replace("-","")
        new_customer.NationalId = f"{formatted_birthday}-{form.national_id.data}"
        new_customer.Telephone = form.telephone.data
        new_customer.TelephoneCountryCode = 55
        new_customer.EmailAddress = form.email.data
        new_customer.Active = True
        db.session.add(new_customer)
        db.session.commit()

        account_a = Account()
        account_a.AccountType = "Personal"
        account_a.Created = datetime.datetime.now()
        account_a.Balance = 0
        account_a.CustomerId = new_customer.Id

        account_b = Account()
        account_b.AccountType = "Checking"
        account_b.Created = datetime.datetime.now()
        account_b.Balance = 0
        account_b.CustomerId = new_customer.Id

        
        db.session.add(account_a)
        db.session.add(account_b)
        db.session.commit()






    return render_template("register_customer.html", form=form)



@app.route("/manage/<id>", methods = ["GET","POST"])
@auth_required()
@roles_accepted("Admin","Cashier")
def manage_customer(id):
    form = Edit_customer_form()
    customer = Customer.query.filter_by(Id=id)
    check_active = Customer.query.filter_by(Id=id).first()
    check_active = check_active.Active


    for i in Customer.query.all():
        if i.Country in form.country.choices:
            break
        form.country.choices.append(i.Country)
    
    if form.validate_on_submit():
        update_customer = Customer.query.filter_by(Id=id).first()
        for i in form.data.items():
            if i[1] == None or i[1] == "" or i[0] == "csrf_token":
                continue
            else:
                if form.first_name.data == i[1]:
                    update_customer.GivenName = form.first_name.data
                elif form.last_name.data == i[1]:
                    update_customer.Surname = form.last_name.data
                elif form.street_address.data == i[1]:
                    update_customer.Streetaddress = form.street_address.data
                elif form.city.data == i[1]:
                    update_customer.City = form.city.data
                elif form.zipcode.data == i[1]:
                    update_customer.Zipcode = form.zipcode.data
                elif form.country.data == i[1]:
                    update_customer.Country = form.country.data
                elif form.telephone.data == i[1]:
                    update_customer.Telephone = form.telephone.data
                elif form.email.data == i[1]:
                    update_customer.EmailAddress = form.email.data

        db.session.commit()
        flash("Customer updated successfully!")
        return redirect("/customer/" + id)
    


    return render_template("/manage_customer.html",customer=customer, form=form, check_active=check_active)



@app.route("/active/<id>")
def deactivate_customer(id):
    customer = Customer.query.filter_by(Id=id).first()
    deactivate = request.args.get('deactivate')
    if deactivate == "true":
        customer.Active = False
        db.session.commit()
        return redirect("/customer/" + id)
    
    if deactivate == "false":
        customer.Active = True
        db.session.commit()
        return redirect("/customer/" + id)

    
    

    





if __name__  == "__main__":
    with app.app_context():
        upgrade()



        seedData(app,db)
        app.run(debug=True)

