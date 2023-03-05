from flask import Flask
from flask_migrate import Migrate, upgrade
from model import db, seedData
from flask_security import current_user


app = Flask(__name__)
app.config.from_object("config.DebugConfig")

db.app = app
db.init_app(app)
migrate = Migrate(app,db)
app.static_folder = 'static'
    
from areas.main_blueprints.main_page import main_page
from areas.account_page_blueprints.account_page import accounts_BP
from areas.customer_page_blueprints.customer_page import customers_BP
from areas.report_page_blueprints.report_page import report_page
from areas.admin_page_blueprints.admin_page import admin_BP
from areas.api.api_blueprints import api_BP

app.register_blueprint(main_page)
app.register_blueprint(accounts_BP)
app.register_blueprint(customers_BP)
app.register_blueprint(report_page)
app.register_blueprint(admin_BP)
app.register_blueprint(api_BP)




if __name__  == "__main__":
    with app.app_context():
        upgrade()
        



        seedData(app,db)
        app.run(debug=True)

