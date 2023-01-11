from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from model import Customer,Account,Transaction

from model import db, seedData

 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:my-secret-pw@localhost/Bank'
db.app = app
db.init_app(app)
migrate = Migrate(app,db)
 



@app.route("/")
def startpage():
    total_customers = len(Customer.query.all())
    total_accounts = len(Account.query.all())
    total_transactions = len(Transaction.query.all())




    return render_template("index.html", total_customers=total_customers,total_accounts=total_accounts,total_transactions=total_transactions)


@app.route("/customers")
def customers():
    customers = Customer.query.all()
    return render_template("customers.html", customers=customers)


@app.route("/customer/<id>")
def customer_page(id):
    customer = Customer.query.filter_by(Id=id).first()
    return render_template("customer.html", customer=customer)


if __name__  == "__main__":
    with app.app_context():
        upgrade()
    
        seedData(db)
        app.run()

