from flask import Blueprint, render_template,flash,url_for
from model import Customer,Account,Transaction
from datetime import datetime
from flask_security import auth_required,roles_accepted
from forms import Issue_report_form,Deposition_form, Withdrawal_form, Transfer_form_internal, Transfer_form_external, Edit_customer_form,Register_customer_form
from flask import request, redirect
from model import db

report_page = Blueprint('report_page', __name__)



@report_page.route("/report-form", methods = ["GET","POST"])
@auth_required()
@roles_accepted("Admin","Cashier")

def report_issue():
    form = Issue_report_form()
    if form.validate_on_submit():
        # todays_date = datetime.now()
        # time_date = todays_date.strftime("%Y-%m-%d %H:%M:%S")
        

        return redirect("/report-confirmation?name=" + form.name.data)

    return render_template("/issue_report.html", form=form)