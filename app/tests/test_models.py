# import os
# import tempfile
import unittest

import my_exceptions
from app import app
from config import configure_app
from models import db

from models_credentials import (  # Customer,; RoomItem,
    Address, Company, RoomItemModifications, User)

# from datetime import datetime


def clear_data(session):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        session.execute(table.delete())
    session.commit()


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        configure_app(app, configuration='testing')
        db.init_app(app)
        self.app = app
        with self.app.app_context():
            db.session.rollback()
            clear_data(db.session)
            # db.drop_all()
            db.create_all()
            self.John = User(
                given_name='John', family_name='Doe', email='john@doe.com')
            self.Gary = User(
                given_name='Gary',
                family_name='McQueen',
                email='gary@mcqueen.com')
            self.CorporationAddress = Address(
                address1='Roady road', post_code=123, post_area='Post place')
            self.BusinessAddress = Address(
                address1='Grimy Road', post_code=1243, post_area='Grimy place')
            self.CustomerAddress = Address(
                address1='Not so Roady road',
                post_code=1235,
                post_area='Not a post place')
            self.Corporation = Company(
                name='Corporation',
                address=self.CorporationAddress,
                orgnumber=123123123)
            self.Business = Company(
                name='Business',
                address=self.BusinessAddress,
                orgnumber=321321321)
            db.session.add(self.Corporation)
            db.session.add(self.Business)
            db.session.add(self.BusinessAddress)
            db.session.add(self.CorporationAddress)
            db.session.add(self.CustomerAddress)
            db.session.add(self.John)
            db.session.add(self.Gary)
            db.session.commit()
            self.John = User.query.filter(User.email == 'john@doe.com').first()
            self.Gary = User.query.filter(
                User.email == 'gary@mcqueen.com').first()
            self.Corporation = Company.query.filter(
                Company.name == 'Corporation').first()
            self.Business = Company.query.filter(
                Company.name == 'Business').first()

    def tearDown(self):
        # self.app = app.test_client()
        pass

    def test_company_duplicate(self):
        """Should fail on creating company with same orgnumber"""
        with self.app.app_context():
            self.assertRaises(
                my_exceptions.MyBaseException,
                Company.update_or_create,
                company_id=None,
                address=self.BusinessAddress,
                name='duplicate',
                description='a dupe',
                orgnumber=123123123,
                lat=1,
                lng=1)


if __name__ == '__main__':
    unittest.main()
