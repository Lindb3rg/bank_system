from flask import Blueprint, render_template,flash,url_for
from model import Customer,Account,Transaction
from datetime import datetime
from flask_security import roles_accepted,auth_required
from forms import Issue_report_form,Deposition_form, Withdrawal_form, Transfer_form_internal, Transfer_form_external, Edit_customer_form,Register_customer_form
from flask import request, redirect
from model import db

customers_BP = Blueprint('customer_BP', __name__)




@customers_BP.route("/customers")
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
    return render_template("customer_templates/customers.html", 
                    listOfCustomers=paginationObject.items, 
                    activePage="customersPage",
                    page=page,
                    sortColumn=sortColumn,
                    sortOrder=sortOrder,
                    has_next = paginationObject.has_next,
                    has_prev = paginationObject.has_prev,
                    pages=paginationObject.pages,
                    q = searchWord)





@customers_BP.route("/customer/<id>")
@auth_required()
@roles_accepted("Admin","Cashier")

def customer_page(id):
    customer = Customer.query.filter_by(Id=id).first()
    accounts = Account.query.filter_by(CustomerId=id)
    total = 0
    for account in accounts:
        total += account.Balance
    


    return render_template("customer_templates/customer.html", customer=customer, accounts=accounts,total=total)






@customers_BP.route("/active/<id>")
@auth_required()
@roles_accepted("Admin","Cashier")
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







@customers_BP.route("/register", methods = ["GET","POST"])
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


    return render_template("customer_templates/register_customer.html", form=form)









@customers_BP.route("/manage/<id>", methods = ["GET","POST"])
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
    


    return render_template("customer_templates/manage_customer.html",customer=customer, form=form, check_active=check_active)