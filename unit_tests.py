import os
import app
import unittest
import tempfile
from config import configure_app

class FlaskrTestCase(unittest.TestCase):

    flaskr.app.config['TESTING'] = True
    configure_app(flaskr)

    def setUp(self):
        self.app = flaskr.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

if __name__ == '__main__':
    unittest.main()
