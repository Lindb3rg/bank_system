import os


class DebugConfig():
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:my-secret-pw@localhost/Bank'
    SECRET_KEY = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-123asdasfasdf')
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT", '851453681323861735056780167285096341234')
    REMEMBER_COOKIE_SAMESITE = "strict"
    SESSION_COOKIE_SAMESITE = "strict"