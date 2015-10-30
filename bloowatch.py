# import flask
from flask import Flask, render_template, request, flash, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from forms import RegisterForm
import re
import os
import json
import logging
from logging import Formatter, FileHandler
import datetime


#######################
#### configuration ####
#######################

app = Flask(__name__)
#Setup the logger
LOGGER = logging.getLogger('opencoast_streamer_logger')
file_handler = FileHandler('opencoast_streamer.log')
handler = logging.StreamHandler()
file_handler.setFormatter(Formatter(
        '%(thread)d %(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
))
handler.setFormatter(Formatter(
        '%(thread)d %(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
))
LOGGER.addHandler(file_handler)
LOGGER.addHandler(handler)
LOGGER.setLevel(logging.DEBUG)

app.config.from_pyfile('_config.py')
db = SQLAlchemy(app)

##########################
#### helper functions ####
##########################


def valid_mail(email):
    match = re.match(r'^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$', str(email))
    if match:
        return True
    else:
        return False

##########################
#######  routes  #########
##########################

@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        #user_email = request.args.get('user_email', 0, type=str)
        user_email = str(request.form['user_email'])
        try:
            if user_email and valid_mail(user_email):
                from models import RegisteredMail
                new_rm = RegisteredMail(
                    user_email,
                    datetime.datetime.utcnow(),
                )
                try:
                    db.session.add(new_rm)
                    db.session.commit()
                    LOGGER.info('User registered correctly, email was ' + user_email)
                    message = 'Thanks for subscribing to Bloowatch, we will keep you posted!'
                    return json.dumps({'status': 'OK', 'message': message})
                except IntegrityError as e:
                    LOGGER.error('User email provided already exists, email was ' + user_email + ' More info'
                                 + str(e))
                    message = 'Provided email is already used, please use a different one.'
                    return json.dumps({'status': 'ERROR', 'message': message})
            else:
                LOGGER.error('Email provided is invalid. It was ' + user_email)
                message = 'Provided email is invalid, please use valid one'
                return json.dumps({'status': 'ERROR', 'message': message})

        except Exception as e:
            LOGGER.error('Unexpected error occured. More info ' + str(e))
            message = 'Unexpected error occured, Please try again later.'
            return json.dumps({'status': 'ERROR', 'message': message})


# Define views for errors
@app.errorhandler(404)
def not_found(error):
    if app.debug is not True:
        now = datetime.datetime.now()
        r = request.url
        with open('error.log', 'a') as f:
            current_timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
            f.write("\n404 error at {}: {}"
                    .format(current_timestamp, r))
    return render_template('error_404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if app.debug is not True:
        now = datetime.datetime.now()
        r = request.url
        with open('error.log', 'a') as f:
            current_timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
            f.write("\n500 error at {}: {}"
                    .format(current_timestamp, r))
    return render_template('error_500.html'), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
