from flask import Blueprint, render_template,request
from model import Customer,Account,db

from flask_security import roles_accepted,auth_required,logout_user
from sqlalchemy import func
from flask import redirect





main_page = Blueprint('main_page', __name__)


@main_page.route("/")
@auth_required()
@roles_accepted("Admin","Cashier")
def startpage():

    US_customers = Customer.query.filter_by(Country="USA").all()
    US_count = len(US_customers)
    US_total_balance = 0
    US_total_accounts = 0
    US_results = db.session.query(Customer, Account).join(Account).filter(Customer.Country=="USA").all()

    for customer,account in US_results:
        US_total_balance += account.Balance
        US_total_accounts += 1



    SE_customers = Customer.query.filter_by(Country="Sweden").all()
    SE_count = len(SE_customers)
    SE_total_balance = 0
    SE_total_accounts = 0
    SE_results = db.session.query(Customer, Account).join(Account).filter(Customer.Country=="Sweden").all()

    for customer,account in SE_results:
        SE_total_balance += account.Balance
        SE_total_accounts += 1




    FI_customers = Customer.query.filter_by(Country="Finland").all()
    FI_count = len(FI_customers)
    FI_total_balance = 0
    FI_total_accounts = 0
    FI_results = db.session.query(Customer, Account).join(Account).filter(Customer.Country=="Finland").all()

    for customer,account in FI_results:
        FI_total_balance += account.Balance
        FI_total_accounts += 1

    NO_customers = Customer.query.filter_by(Country="Norway").all()
    NO_count = len(NO_customers)

    NO_total_balance = 0
    NO_total_accounts = 0
    NO_results = db.session.query(Customer, Account).join(Account).filter(Customer.Country=="Norway").all()

    for customer,account in NO_results:
        NO_total_balance += account.Balance
        NO_total_accounts += 1
   
    


    
    return render_template("/main_templates/start_page.html", US_count=US_count,
                           US_total_balance = US_total_balance,
                           US_total_accounts = US_total_accounts,
                           SE_count=SE_count,
                           SE_total_accounts = SE_total_accounts,
                           SE_total_balance = SE_total_balance,

                           FI_count=FI_count,
                           FI_total_accounts = FI_total_accounts,
                           FI_total_balance = FI_total_balance,
                           NO_count=NO_count,
                           NO_total_accounts = NO_total_accounts,
                           NO_total_balance = NO_total_balance)



# @main_page.route("/top_10", methods=["GET"])
# def more_transactions():
#     transaction_list=[]
#     country = request.args.get('country')
#     results = db.session.query(Customer, Account).join(Account).filter(Customer.Country== country).all()
#     for result in results:

    

    


   
    # for transaction in transactions.items:
    #     t = { "Id": transaction.Id,"Type":transaction.Type, "Operation":transaction.Operation, "Date": transaction.Date, "Amount":transaction.Amount,"NewBalance":transaction.NewBalance }
    #     transaction_list.append(t)
    # return jsonify(transaction_list)



@main_page.route("/logout")
def logout():
    logout_user()
    return redirect("/")