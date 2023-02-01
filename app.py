from flask import Flask, render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from model import Customer,Account,Transaction
from sqlalchemy import func
from flask_security import roles_accepted, auth_required, logout_user
import os
from model import db, seedData




app = Flask(__name__)
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

@app.route("/report-form", methods = ["GET","POST"])
def report_issue():
    form = report_form()
    if form.validate_on_submit():
        return redirect("/report-confirmation?FirstName=" + form.fname.data)

    return render_template("/issue_report.html", form=form)





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


if __name__  == "__main__":
    with app.app_context():
        upgrade()


        seedData(app,db)
        app.run(debug=True)

