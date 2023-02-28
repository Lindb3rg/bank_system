from flask import Flask
from flask_migrate import Migrate, upgrade
from model import db, seedData


app = Flask(__name__)
app.config.from_object("config.DebugConfig")

db.app = app
db.init_app(app)
migrate = Migrate(app,db)
    
from areas.main_blueprints.main_page import main_page
from areas.account_page_blueprints.account_page import accounts_BP
from areas.customer_page_blueprints.customer_page import customers_BP
from areas.report_page_blueprints.report_page import report_page

app.register_blueprint(main_page)
app.register_blueprint(accounts_BP)
app.register_blueprint(customers_BP)
app.register_blueprint(report_page)




if __name__  == "__main__":
    with app.app_context():
        upgrade()



        seedData(app,db)
        app.run(debug=True)

