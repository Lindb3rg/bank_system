import unittest
from flask import Flask
from app import app
from model import db, Customer, User,Role,Account
from flask_security import Security,SQLAlchemyUserDatastore, hash_password
from datetime import datetime



init = False

class FormsTestCases(unittest.TestCase):

    def tearDown(self):
        self.ctx.pop()
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        app.config["SERVER_NAME"] = "adam.se"
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['WTF_CSRF_METHODS'] = []  # This is the magic
        app.config['TESTING'] = True
        app.config['LOGIN_DISABLED'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['SECURITY_FRESHNESS_GRACE_PERIOD'] = 123454
        global init
        if not init:
            db.init_app(app)
            db.create_all()
            init = True
            user_datastore = SQLAlchemyUserDatastore(db, User, Role)
            app.security = Security(app, user_datastore,register_blueprint=False)
            app.security.init_app(app, user_datastore,register_blueprint=False)
            app.security.datastore.db.create_all()




   












    # def test_when_withdrawing_more_than_balance_should_show_errormessage(self):

    #     customer = Customer()
    #     customer.GivenName = "Kalle"
    #     customer.Surname = "Anka"
    #     customer.Streetaddress = "Gatan1"
    #     customer.City = "Ankeborg"
    #     customer.Zipcode = "12345"
    #     customer.Country = "Gåseborg"
    #     customer.CountryCode = "55"
    #     customer.Birthday = datetime.now()
    #     customer.NationalId = "12344"
    #     customer.TelephoneCountryCode = 45
    #     customer.Telephone = "12343"
    #     customer.EmailAddress = "kalle@anka.se"
    #     customer.Active = True


    #     db.session.add(customer)
    #     db.session.commit()

    #     account_a = Account()
    #     account_a.AccountType = "personal"
    #     account_a.Balance = 200
    #     account_a.Created = datetime.now()
    #     account_a.CustomerId = customer.Id
    #     db.session.add(account_a)
    #     db.session.commit()

    #     test_client = app.test_client()
    #     user = User.query.get(1)
    #     with test_client:
    #         url = '/withdraw/' + str(account_a.Id)
    #         response = test_client.post(url, data={ "current_balance":"200", "amount":"300","is_active":"True","Type":"Payment","confirmation":"True"})
    #         s = response.data.decode("utf-8") 
    #         ok = 'Not enough funds' in s
    #         self.assertTrue(ok)














    # def test_when_depositing_more_than_15k_should_show_errormessage(self):

    #     customer = Customer()
    #     customer.GivenName = "Kalle"
    #     customer.Surname = "Anka"
    #     customer.Streetaddress = "Gatan1"
    #     customer.City = "Ankeborg"
    #     customer.Zipcode = "12345"
    #     customer.Country = "Gåseborg"
    #     customer.CountryCode = "55"
    #     customer.Birthday = datetime.now()
        # customer.NationalId = "12344"
        # customer.TelephoneCountryCode = 45
        # customer.Telephone = "12343"
        # customer.EmailAddress = "kalle@anka.se"
        # customer.Active = True


        # db.session.add(customer)
        # db.session.commit()

        # account_a = Account()
        # account_a.AccountType = "personal"
        # account_a.Balance = 200
        # account_a.Created = datetime.now()
        # account_a.CustomerId = customer.Id
        # db.session.add(account_a)
        # db.session.commit()

        # test_client = app.test_client()
        # user = User.query.get(1)
        # with test_client:
        #     url = '/deposit/' + str(account_a.Id)
        #     response = test_client.post(url, data={ "deposition":"16000", "type":"Salary","confirmation":"True","is_active":"True"})
        #     s = response.data.decode("utf-8") 
        #     ok = 'Deposition limit 15000 SEK' in s
        #     self.assertTrue(ok)
    










    # def test_when_depositing_less_than_0_should_show_errormessage(self):

    #     customer = Customer()
    #     customer.GivenName = "Kalle"
    #     customer.Surname = "Anka"
    #     customer.Streetaddress = "Gatan1"
    #     customer.City = "Ankeborg"
    #     customer.Zipcode = "12345"
    #     customer.Country = "Gåseborg"
    #     customer.CountryCode = "55"
    #     customer.Birthday = datetime.now()
    #     customer.NationalId = "12344"
    #     customer.TelephoneCountryCode = 45
    #     customer.Telephone = "12343"
    #     customer.EmailAddress = "kalle@anka.se"
    #     customer.Active = True


    #     db.session.add(customer)
    #     db.session.commit()

    #     account_a = Account()
    #     account_a.AccountType = "personal"
    #     account_a.Balance = 200
    #     account_a.Created = datetime.now()
    #     account_a.CustomerId = customer.Id
    #     db.session.add(account_a)
    #     db.session.commit()

    #     test_client = app.test_client()
    #     user = User.query.get(1)
    #     with test_client:
    #         url = '/deposit/' + str(account_a.Id)
    #         response = test_client.post(url, data={ "deposition":"0", "type":"Salary","confirmation":"True","is_active":"True"})
    #         s = response.data.decode("utf-8") 
    #         ok = 'Cannot use negative values. Must be at least 1 SEK' in s
    #         self.assertTrue(ok)

    
    













    # def test_when_depositing_without_confirmation_should_show_errormessage(self):

    #     customer = Customer()
    #     customer.GivenName = "Kalle"
    #     customer.Surname = "Anka"
    #     customer.Streetaddress = "Gatan1"
    #     customer.City = "Ankeborg"
    #     customer.Zipcode = "12345"
    #     customer.Country = "Gåseborg"
    #     customer.CountryCode = "55"
    #     customer.Birthday = datetime.now()
    #     customer.NationalId = "12344"
    #     customer.TelephoneCountryCode = 45
    #     customer.Telephone = "12343"
    #     customer.EmailAddress = "kalle@anka.se"
    #     customer.Active = True


    #     db.session.add(customer)
    #     db.session.commit()

    #     account_a = Account()
    #     account_a.AccountType = "personal"
    #     account_a.Balance = 200
    #     account_a.Created = datetime.now()
    #     account_a.CustomerId = customer.Id
    #     db.session.add(account_a)
    #     db.session.commit()

    #     test_client = app.test_client()
    #     user = User.query.get(1)
    #     with test_client:
    #         url = '/deposit/' + str(account_a.Id)
    #         response = test_client.post(url, data={ "deposition":"500", "type":"Salary","confirmation":"false","is_active":"True"})
    #         s = response.data.decode("utf-8") 
    #         ok = 'Confirmation needed!' in s
    #         self.assertTrue(ok)












    # def test_when_using_negative_numbers_or_zero_should_show_errormessage(self):

    #     customer = Customer()
    #     customer.GivenName = "Kalle"
    #     customer.Surname = "Anka"
    #     customer.Streetaddress = "Gatan1"
    #     customer.City = "Ankeborg"
    #     customer.Zipcode = "12345"
    #     customer.Country = "Gåseborg"
    #     customer.CountryCode = "55"
    #     customer.Birthday = datetime.now()
    #     customer.NationalId = "12344"
    #     customer.TelephoneCountryCode = 45
    #     customer.Telephone = "12343"
    #     customer.EmailAddress = "kalle@anka.se"
    #     customer.Active = True


    #     db.session.add(customer)
    #     db.session.commit()

    #     account_a = Account()
    #     account_a.AccountType = "personal"
    #     account_a.Balance = 200
    #     account_a.Created = datetime.now()
    #     account_a.CustomerId = customer.Id
    #     db.session.add(account_a)
    #     db.session.commit()

    #     test_client = app.test_client()
    #     user = User.query.get(1)
    #     with test_client:
    #         url = '/deposit/' + str(account_a.Id)
    #         response = test_client.post(url, data={ "deposition":"0", "type":"Salary","confirmation":"true","is_active":"True"})
    #         s = response.data.decode("utf-8") 
    #         ok = 'Cannot use negative values. Must be at least 1 SEK' in s
    #         self.assertTrue(ok)












    # def test_when_external_without_exising_reciever_should_show_errormessage(self):

    #         customer = Customer()
    #         customer.GivenName = "Kalle"
    #         customer.Surname = "Anka"
    #         customer.Streetaddress = "Gatan1"
    #         customer.City = "Ankeborg"
    #         customer.Zipcode = "12345"
    #         customer.Country = "Gåseborg"
    #         customer.CountryCode = "55"
    #         customer.Birthday = datetime.now()
    #         customer.NationalId = "12344"
    #         customer.TelephoneCountryCode = 45
    #         customer.Telephone = "12343"
    #         customer.EmailAddress = "kalle@anka.se"
    #         customer.Active = True


    #         db.session.add(customer)
    #         db.session.commit()

    #         account_a = Account()
    #         account_a.AccountType = "personal"
    #         account_a.Balance = 500
    #         account_a.Created = datetime.now()
    #         account_a.CustomerId = customer.Id
    #         db.session.add(account_a)
    #         db.session.commit()


    #         test_client = app.test_client()
    #         user = User.query.get(1)
    #         with test_client:
    #             url = '/external/' + str(account_a.Id)
    #             response = test_client.post(url, data={ "current_balance":"", "account_to":"4","amount":"200","confirmation":"true","is_active":"true"})
    #             s = response.data.decode("utf-8") 
    #             ok = 'Customer not existing' in s
    #             self.assertTrue(ok)









    # def test_when_transfer_to_same_account_should_show_errormessage(self):

    #     customer = Customer()
    #     customer.GivenName = "Kalle"
    #     customer.Surname = "Anka"
    #     customer.Streetaddress = "Gatan1"
    #     customer.City = "Ankeborg"
    #     customer.Zipcode = "12345"
    #     customer.Country = "Gåseborg"
    #     customer.CountryCode = "55"
    #     customer.Birthday = datetime.now()
    #     customer.NationalId = "12344"
    #     customer.TelephoneCountryCode = 45
    #     customer.Telephone = "12343"
    #     customer.EmailAddress = "kalle@anka.se"
    #     customer.Active = True


    #     db.session.add(customer)
    #     db.session.commit()

    #     account_a = Account()
    #     account_a.AccountType = "personal"
    #     account_a.Balance = 500
    #     account_a.Created = datetime.now()
    #     account_a.CustomerId = customer.Id
    #     db.session.add(account_a)
    #     db.session.commit()


    #     test_client = app.test_client()
    #     user = User.query.get(1)
    #     with test_client:
    #         url = '/external/' + str(account_a.Id)
    #         response = test_client.post(url, data={ "current_account":"1","current_balance":"", "account_to":"1","amount":"200","confirmation":"true","is_active":"true"})
    #         s = response.data.decode("utf-8") 
    #         ok = 'Cannot transfer to same account' in s
    #         self.assertTrue(ok)














if __name__ == "__main__":
    unittest.main()

