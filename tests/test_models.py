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
            form_data = {"Adresse installasjonssted": "Kingsroad 1", "Firmanavn": "Kristiansand Elektro AS", "Organisasjonsnr": "980 489 590", "Adresse Installat\u00f8r": "Rigetj\u00f8nnveien 3, 4626 Kristiansand S", "Eks bad, gang": "Kings room", "gulv": "Ja", "Styr": "Ja", "Mont": "Ja", "Jord": "Ja", "Type kabel/matte": "\u00d8S-30-21-16Wm", "Areal m2": 900, "c/c": 6428.57,
                         "Spenning V": 230, "Resistans min \u2126": 228, "Resistans max \u2126": 265, "Resistans \u2126 inst": 1, "Resistans \u2126 st\u00f8p": 2, "Isolasjonstest M\u2126 st\u00f8p": 999, "Resistans \u2126 tilk": 3, "Isolasjonstest M\u2126 inst": 999, "Isolasjonstest M\u2126 tilk": 999, "Eier": "Ja", "Doku": "Ja", "Dag": "18", "Mnd": "06", "\u00c5r": "2017"}
            request_form = {"anleggs_adresse": "Kingsroad 1", "anleggs_poststed": "Kings place", "anleggs_postnummer": "4321", "rom_navn": "Kings room", "areal": "1000",
                            "oppvarmet_areal": "900", "mohm_a": "true", "mohm_b": "true", "mohm_c": "true", "ohm_a": "1", "ohm_b": "2", "ohm_c": "3", "product_id": "3"}
            self.testForm = FilledForm.update_or_create(
                filled_form_id=None,
                user=self.John,
                name='Awesome form',
                customer_name='Awesome customer',
                request_form=request_form,
                form_data=form_data,
                company=self.Corporation,
                address=self.CustomerAddress
            )
            self.testForm2 = FilledForm.update_or_create(
                filled_form_id=None,
                user=self.Gary,
                name='Boring form',
                customer_name='Boring customer',
                request_form=request_form,
                form_data=form_data,
                company=self.Business,
                address=self.CustomerAddress
            )
            self.testForm3 = FilledForm.update_or_create(
                filled_form_id=None,
                user=self.Gary,
                name='Ok form',
                customer_name='form customer',
                request_form=request_form,
                form_data=form_data,
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
            self.Gary = User.query.filter(
                User.email == 'gary@mcqueen.com').first()
            self.Corporation = Company.query.filter(
                Company.name == 'Corporation').first()
            self.Business = Company.query.filter(
                Company.name == 'Business').first()

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
            self.assertEqual(
                result[0]
                .filled_form.name,
                'Boring form')
            self.assertEqual(
                result[0]
                .user.email,
                'gary@mcqueen.com')
            self.assertEqual(
                result[0]
                .filled_form_data.request_form['anleggs_adresse'],
                'Kingsroad 1')
            self.assertEqual(
                result[0]
                .filled_form_data.form_data['Adresse installasjonssted'],
                'Kingsroad 1')
            result = self.Corporation.get_forms()
            self.assertEqual(len(result), 2)

if __name__ == '__main__':
    unittest.main()
