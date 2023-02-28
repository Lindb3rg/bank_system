from flask import Blueprint, render_template,flash,url_for
from model import Customer,Account,Transaction
from datetime import datetime
from flask_security import roles_accepted,auth_required,logout_user
from forms import Issue_report_form,Deposition_form, Withdrawal_form, Transfer_form_internal, Transfer_form_external, Edit_customer_form,Register_customer_form
from flask import request, redirect
from model import db
from sqlalchemy import func



main_page = Blueprint('main_page', __name__)


@main_page.route("/")
@auth_required()
@roles_accepted("Admin","Cashier")
def startpage():
    total_customers = len(Customer.query.all())
    total_accounts = len(Account.query.all())
    total_balance = Account.query.with_entities(func.sum(Account.Balance).label('total')).first().total
    rounded_total_balance = round(total_balance, 2)

    
    return render_template("start_page.html", total_customers=total_customers,total_accounts=total_accounts,rounded_total_balance=rounded_total_balance)




@main_page.route("/logout")
def logout():
    logout_user()
    return redirect("/")