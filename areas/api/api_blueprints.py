from flask import Blueprint,jsonify
from flask import request
from model import Customer,Account



api_BP = Blueprint('api_BP', __name__)







@api_BP.route("/api/<id>")
def customer_api(id):
    customer_data=[]
    current_customer = Customer.query.filter_by(Id=id)
    
    for data in current_customer:
        t = { "id": data.Id,
             "first_name":data.GivenName,
             "last_name":data.Surname,
             "street_address": data.Streetaddress,
             "city":data.City,
             "zipcode":data.Zipcode,
             "country":data.Country,
             "country_code":data.CountryCode,
             "birthday":data.Birthday,
             "national_id":data.NationalId,
             "telephone_country_code":data.TelephoneCountryCode,
             "telephone":data.Telephone,
             "email_address":data.EmailAddress,
             "active":data.Active,
            
            }
        customer_data.append(t)
        for account in data.Accounts:
            a = {"account_id":account.Id,
                 "account_type":account.AccountType,
                 "created":account.Created,
                 "balance":account.Balance,
                 "customer_id":account.CustomerId
                 }
            customer_data.append(a)
    return jsonify(customer_data)




@api_BP.route("/api/account/<id>", methods=["GET"])
def transaction_api(id):
    transaction_data=[]
    current_account = Account.query.filter_by(Id=id).first()
    limit = int(request.args.get('limit',""))
    offset = int(request.args.get('offset',""))
    
    sliced_data = current_account.Transactions[offset:limit+offset]
    for data in sliced_data:
        t = { "transaction_id": data.Id,
            "transaction_type":data.Type,
            "operation":data.Operation,
            "date": data.Date,
            "amount":data.Amount,
            "new_balance":data.NewBalance,
            "account_id":data.AccountId,
            }
        transaction_data.append(t)

  
       
    return jsonify(transaction_data)

#  