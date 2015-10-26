from flask import Flask, redirect, flash, redirect, render_template, \
    request, url_for, make_response, jsonify, session
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from forms import RegisterForm
import re
import datetime
import os


'''@app.route('/')
def main():
    return 'Hello World!'
'''

#######################
#### configuration ####
#######################

app = Flask(__name__)
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
    if request.args and 'email' in request.args:
        session['user_email'] = request.args['email']
        return redirect(url_for('register'))
    else:
        form = RegisterForm()
    return render_template('index.html',
                           title="Register",
                           form=form)
    #redirect(url_for('_base'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    error = None
    email = session['user_email']
    session.clear()
    try:
        form = RegisterForm(email=email)
        if form.email.data and valid_mail(form.email.data):
            from models import RegisteredMail
            new_rm = RegisteredMail(
                form.email.data,
                datetime.datetime.utcnow(),
            )
            try:
                db.session.add(new_rm)
                db.session.commit()
                flash('Thanks for subscribing to Bloowatch, we will keep you posted!', 'success')
                return redirect(url_for('main'))
            except IntegrityError:
                flash('Provided email is already used, please use a different one', 'error')
                return redirect(url_for('main'))
        else:
            flash('Provided email is invalid, please use valid one', 'error')
            return redirect(url_for('main'))
    except Exception as e:
        print e
        return render_template('index.html', form=form, error=error)

################
#### routes ####
################

@app.route('/api/v1/registered_mails/')
def api_registered_mails():
    from models import RegisteredMail
    results = db.session.query(RegisteredMail).limit(10).offset(0).all()
    json_results = []
    for result in results:
        data = {
            'registered_mail_id': result.registered_id,
            'email': result.email,
            'creation date': str(result.creation_date)
        }
        json_results.append(data)
    return jsonify(items=json_results)

@app.route('/api/v1/registered_mails/<int:registered_id>')
def registered_mail(registered_id):
    from models import RegisteredMail
    result = db.session.query(RegisteredMail).filter_by(registered_id=registered_id).first()
    if result:
        result = {
            'registered_mail_id': result.registered_id,
            'email': result.email,
            'creation date': str(result.creation_date)
        }
        code = 200
    else:
        result = {'error': 'Specified registered mail does not exist'}
        code = 404
    return make_response(jsonify(result), code)

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


