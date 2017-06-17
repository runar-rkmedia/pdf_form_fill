import os
from app import app
import unittest
import tempfile
from config import configure_app
from models import User, FilledForm, db, Company, Address


class FlaskrTestCase(unittest.TestCase):
    #

    def setUp(self):
        configure_app(app, configuration='testing')
        db.init_app(app)
        self.app = app
        with self.app.app_context():
            db.drop_all(bind=None)
            db.create_all(bind=None)
            self.John = User(
                given_name='John',
                family_name='Doe',
                email='john@doe.com'
            )
            self.Gary = User(
                given_name='Gary',
                family_name='McQueen',
                email='gary@mcqueen.com'
            )
            self.CorporationAddress = Address(
                line1='Roady road',
                postnumber=123,
                postal='Post place')
            self.BusinessAddress = Address(
                line1='Grimy Road',
                postnumber=1243,
                postal='Grimy place'
            )
            self.CustomerAddress = Address(
                line1='Not so Roady road',
                postnumber=1235,
                postal='Not a post place'
            )
            self.Corporation = Company(
                name='Corporation',
                address=self.CorporationAddress
            )
            self.Business = Company(
                name='Business',
                address=self.BusinessAddress
            )
            testForm = {"anleggs_adresse": "test", 'product_id': 129}
            self.testForm = FilledForm.update_or_create(
                filled_form_id=None,
                user=self.John,
                name='Awesome form',
                customer_name='Awesome customer',
                data=testForm,
                company=self.Corporation,
                address=self.CustomerAddress
            )
            self.testForm2 = FilledForm.update_or_create(
                filled_form_id=None,
                user=self.Gary,
                name='Boring form',
                customer_name='Boring customer',
                data=testForm,
                company=self.Business,
                address=self.CustomerAddress
            )
            self.testForm3 = FilledForm.update_or_create(
                filled_form_id=None,
                user=self.Gary,
                name='Ok form',
                customer_name='form customer',
                data=testForm,
                company=self.Corporation,
                address=self.CustomerAddress
            )

            db.session.add(self.Corporation)
            db.session.add(self.Business)
            db.session.add(self.BusinessAddress)
            db.session.add(self.CorporationAddress)
            db.session.add(self.CustomerAddress)
            db.session.add(self.testForm)
            db.session.add(self.John)
            db.session.add(self.Gary)
            db.session.commit()
            self.John = User.query.filter(User.email == 'john@doe.com').first()
            self.Gary = User.query.filter(User.email == 'gary@mcqueen.com').first()
            self.Corporation = Company.query.filter(Company.name == 'Corporation').first()
            self.Business = Company.query.filter(Company.name == 'Business').first()

    def tearDown(self):
        # self.app = app.test_client()
        pass

    def test_user_get_form(self):
        """user.getform should return all forms from user."""
        with self.app.app_context():
            result = self.John.get_forms()
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0].filled_form.name, 'Awesome form')
            self.assertEqual(result[0].user.email, 'john@doe.com')
            result = self.Gary.get_forms()
            self.assertEqual(len(result), 2)

    def test_company_get_form(self):
        """company.getform should return all forms from this company."""
        with self.app.app_context():
            result = self.Business.get_forms()
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0].filled_form.name, 'Boring form')
            self.assertEqual(result[0].user.email, 'gary@mcqueen.com')
            result = self.Corporation.get_forms()
            self.assertEqual(len(result), 2)

if __name__ == '__main__':
    unittest.main()
