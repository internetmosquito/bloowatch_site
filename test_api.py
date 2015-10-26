__author__ = 'mosquito'
import os
import unittest
import datetime

from views import app, db
from _config import basedir
from models import RegisteredMail

TEST_DB = 'test.db'


class APITests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

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
        db.session.remove()
        db.drop_all()

    ########################
    #### helper methods ####
    ########################

    def add_registered_users(self):
        ru = RegisteredMail(
            'darthvader@thedarkside.com',
            datetime.datetime.utcnow(),
        )
        db.session.add(ru)
        db.session.commit()
        new_ru = RegisteredMail(
            'lukeskywalker@thebrightside.com',
            datetime.datetime.utcnow(),
        )
        db.session.add(new_ru)
        db.session.commit()

    ###############
    #### tests ####
    ###############

    def test_collection_endpoint_returns_correct_data(self):
        self.add_registered_users()
        response = self.app.get('api/v1/registered_mails/', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.mimetype, 'application/json')
        self.assertIn(b'darthvader@thedarkside.com', response.data)
        self.assertIn(b'lukeskywalker@thebrightside.com', response.data)

    def test_resource_endpoint_returns_correct_data(self):
        self.add_registered_users()
        response = self.app.get('api/v1/registered_mails/2', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.mimetype, 'application/json')
        self.assertIn(b'darthvader@thedarkside.com', response.data)
        self.assertNotIn(b'lukeskywalker@thebrightside.com', response.data)

    def test_invalid_resource_endpoint_returns_error(self):
        self.add_registered_users()
        response = self.app.get('api/v1/registered_mails/999',
                                follow_redirects=True)
        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.mimetype, 'application/json')
        self.assertIn(b'Specified registered mail does not exist', response.data)

    if __name__ == "__main__":
        unittest.main()