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

    # US_customers = Customer.query.filter_by(Country="USA").all()
    # US_count = len(US_customers)
    US_results = db.session.query(Customer, Account).join(Account).filter(Customer.Country=="USA").all()
    US_count = len(US_results.Accounts)


    SE_customers = Customer.query.filter_by(Country="Sweden").all()
    SE_count = len(SE_customers)

    FI_customers = Customer.query.filter_by(Country="Finland").all()
    FI_count = len(FI_customers)

    NO_customers = Customer.query.filter_by(Country="Norway").all()
    NO_count = len(NO_customers)
   
    


    
    return render_template("/main_templates/start_page.html", US_count=US_count,
                           SE_count=SE_count,
                           FI_count=FI_count,
                           NO_count=NO_count)



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