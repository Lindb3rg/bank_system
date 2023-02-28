from flask import Blueprint, render_template
from flask_security import auth_required,roles_accepted
from forms import Issue_report_form
from flask import redirect


report_page = Blueprint('report_page', __name__)



@report_page.route("/report-form", methods = ["GET","POST"])
@auth_required()
@roles_accepted("Admin","Cashier")

def report_issue():
    form = Issue_report_form()
    if form.validate_on_submit():
        # todays_date = datetime.now()
        # time_date = todays_date.strftime("%Y-%m-%d %H:%M:%S")
        

        return redirect("report_page_templates/report-confirmation?name=" + form.name.data)

    return render_template("report_page_templates/issue_report.html", form=form)