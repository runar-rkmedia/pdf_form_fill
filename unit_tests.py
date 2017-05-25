import os
from app import app
import unittest
import tempfile
from config import configure_app



class FlaskrTestCase(unittest.TestCase):

    app.config['TESTING'] = True
    configure_app(app)

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

if __name__ == '__main__':
    unittest.main()
