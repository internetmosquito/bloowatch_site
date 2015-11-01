__author__ = 'mosquito'
import os

# grabs the folder where the script runs
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'bloowatch.db'

DEBUG = False

# defines the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)

# the database uri
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH

MAIL_SERVER = 'smtp.xxx.com'

MAIL_PORT = 465

MAIL_USER = 'info@xxx.com'

MAIL_FROM = 'info@xxx.com'

MAIL_TO = ''

MAIL_PASSWORD = 'xxx'

get_var = globals().get