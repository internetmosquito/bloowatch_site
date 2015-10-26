__author__ = 'mosquito'
import os
import unittest

from views import app, db
from _config import basedir
from models import RegisteredMail

TEST_DB = 'test.db'

class MainTests(unittest.TestCase):

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

    ###############
    #### tests ####
    ###############

    def test_404_error(self):
        response = self.app.get('/this-route-does-not-exist/')
        self.assertEquals(response.status_code, 404)

    def test_index(self):
        response = self.app.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    '''def test_500_error(self):
        bad_user = User(
            name='EddieVedder',
            email='eddievedder@pearljam.com',
            password='pearljam'
        )
        db.session.add(bad_user)
        db.session.commit()
        response = self.login('EddieVedder', 'pearljam')
        self.assertEquals(response.status_code, 500)
        self.assertNotIn(b'ValueError: Invalid salt', response.data)
        self.assertIn(b'Something went terribly wrong.', response.data)'''

if __name__ == "__main__":
    unittest.main()