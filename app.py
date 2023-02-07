from flask import Flask, render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from model import Customer,Account,Transaction
from sqlalchemy import func
from flask_security import roles_accepted, auth_required, logout_user
import os
from model import db, seedData
from forms import Issue_report_form,Deposition_form, Withdrawal_form, Transfer_form
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
    return render_template("start_page.html", total_customers=total_customers,total_accounts=total_accounts,total_balance=total_balance)




@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")





    



@app.route("/customers")
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
def customer_page(id):
    customer = Customer.query.filter_by(Id=id).first()
    accounts = Account.query.filter_by(CustomerId=id)
    


    return render_template("customer.html", customer=customer, accounts=accounts)


@app.route("/account/<customer>/<id>")
def account_page(customer,id):
    id = int(id)
    customer = customer
    account = Account.query.filter_by(Id=id)
    current_transactions = Transaction.query.filter_by(AccountId=id)
    current_transactions = current_transactions.order_by(Transaction.Id.desc())
    
    

    return render_template("account.html", id=id, customer = customer, account=account, current_transactions=current_transactions)





### DEPOSIT ### Deposit cash, Salary, Transfer
@app.route("/deposit/<id>", methods = ["GET","POST"])
def deposit(id):
    id = int(id)
    
    new_deposit = Deposition_form()
    if new_deposit.validate_on_submit():
        account = Account.query.filter_by(Id=id)
        deposit = Transaction()
        deposit.AccountId = id
        deposit.Type = "Debit"
        deposit.Operation = new_deposit.type.data
        deposit.Date = datetime.datetime.now()
        deposit.Amount = new_deposit.deposition.data
        for i in account:
            deposit.NewBalance = i.Balance + new_deposit.deposition.data
            i.Balance += new_deposit.deposition.data
        
        db.session.add(deposit)
        db.session.commit()


        return redirect("/deposition-confirmation")


    return render_template("deposit.html", new_deposit=new_deposit)

@app.route("/deposition-confirmation")
def deposition_confirmation():
    amount = request.args.get("deposition", " ")
    return render_template("/deposition_confirmation.html", deposition=amount)



### WITHDRAW ### Payment, Transfer
@app.route("/withdraw/<id>", methods = ["GET","POST"])
def withdraw(id):
    id = int(id)
    new_withdrawal = Withdrawal_form()
    if new_withdrawal.validate_on_submit():
        account = Account.query.filter_by(Id=id)

        withdraw = Transaction()
        withdraw.AccountId = id
        withdraw.Type = "Credit"
        withdraw.Operation = new_withdrawal.type.data
        withdraw.Date = datetime.datetime.now()
        withdraw.Amount = new_withdrawal.withdrawal.data
        for i in account:
            withdraw.NewBalance = i.Balance - new_withdrawal.withdrawal.data
            i.Balance -= new_withdrawal.withdrawal.data
        
        db.session.add(withdraw)
        db.session.commit()

        return redirect("/withdrawal-confirmation")


    return render_template("withdraw.html", new_withdrawal=new_withdrawal)


@app.route("/withdrawal-confirmation")
def withdrawal_confirmation():

    # amount = request.args.get("deposition", " ")
    return render_template("/withdrawal_confirmation.html")



####### Håller på med transfer. Första ska vara ifyllt automatiskt



### TRANSFER ### Transfer + and -
### accounts_from - amount > new transaction
### accounts_to + amount > new transaction
@app.route("/transfer/<customer_id>/<account_from>", methods = ["GET","POST"])
def transfer(customer_id,account_from):
    customer_id = int(customer_id)
    account_from = int(account_from)
    new_transfer = Transfer_form()


    customer_accounts = Customer.query.filter_by(Id=customer_id)

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

        return redirect("/transfer-confirmation")
    

    return render_template("transfer.html", account_from = account_from, new_transfer=new_transfer)


@app.route("/transfer-confirmation")
def transfer_confirmation():
    return render_template("/transfer_confirmation.html")



### REPORT ###
@app.route("/report-form", methods = ["GET","POST"])
def report_issue():
    form = Issue_report_form()
    if form.validate_on_submit():
        # todays_date = datetime.now()
        # time_date = todays_date.strftime("%Y-%m-%d %H:%M:%S")
        

        return redirect("/report-confirmation?name=" + form.name.data)

    return render_template("/issue_report.html", form=form)


@app.route("/report-confirmation")
def report_confirmation():
    # user_name = request.args.get("name", " ")
    return render_template("/report_confirmation.html")





if __name__  == "__main__":
    with app.app_context():
        upgrade()


        seedData(app,db)
        app.run(debug=True)

