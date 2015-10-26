__author__ = 'mosquito'
import os
import unittest
import datetime

from views import app, db
from _config import basedir
from models import RegisteredMail


TEST_DB = 'test.db'


class RegisteredMailTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

        self.assertEquals(app.debug, False)

    # executed after to each test
    def tearDown(self):
        db.drop_all()

    ########################
    #### helper methods ####
    ########################

    def register_mail(self, email=None, creation_time=None):
        return self.app.post(
            'register/',
            data=dict(
                email=email,
                creation_time=datetime.datetime.utcnow(),
            ),
            follow_redirects=True
        )

    ###############
    #### forms ####
    ###############

    def test_valid_email_is_registered(self):
        self.register_mail('judaspriest@isthebest.com')
        response = self.app.get('/', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn('Thanks for subscribing to Bloowatch, we will keep you posted!', response.data)

    def test_invalid_email_is_registered(self):
        self.register_mail('judaspriest@isthebest.com')
        response = self.app.get('/', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn('Provided email is invalid, please use a different one', response.data)

    ################
    #### models ####
    ################

    def test_string_representation_of_the_registered_email_object(self):

        from datetime import date
        db.session.add(
            RegisteredMail(
                "blabla@bloblo.com",
                date(2015, 2, 14),
            )
        )

        db.session.commit()

        mails = db.session.query(RegisteredMail).all()
        #print appointments
        for mail in mails:
            self.assertEquals(mail.email, 'blabla@bloblo.com')


if __name__ == "__main__":
    unittest.main()
