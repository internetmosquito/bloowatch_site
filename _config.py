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

MAIL_SERVER = 'smtp.zoho.com'

MAIL_PORT = 465

MAIL_USER = 'info@bloowatch.com'

MAIL_FROM = 'info@bloowatch.com'

MAIL_TO = ''

MAIL_PASSWORD = 'EnjX67Zp8qPkLBlmhew4iE1n'

get_var = globals().get