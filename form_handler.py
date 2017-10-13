# -*- coding: utf-8 -*-
"""Create forms from database-objects."""

import os
import string

from dateutil.parser import parse

import my_exceptions
from models_credentials import Customer, Room, RoomItem
from models_product import ProductCatagory
from pdf_filler.helpers import NumberFormatter, OhmsLaw
from pdf_filler.schema import get_template_schema
from pdffields.fields import combine_pdfs
from setup_app import user_file_path


def flatten_dict(d):
    """Flattens a dictionary."""

    def items():
        """Helper-function for flattening."""
        for key, value in d.items():
            if isinstance(value, dict):
                for subkey, subvalue in flatten_dict(value).items():
                    yield key + "." + subkey, subvalue
            else:
                yield key, value

    return dict(items())


class MultiForms(object):
    """Create multiple pdf-forms recursively, depending on input."""

    def __init__(self,
                 entity,
                 user,
                 stamp=None,
                 out=None,
                 create_if_archived=False):
        self.path = user_file_path(create_random_dir=True)
        self.create_if_archived = create_if_archived
        self.files = []
        self.user = user
        self.stamp = stamp
        self.multi_handlers = {}
        if isinstance(entity, RoomItem):
            self.retrieve_by_room_item(entity, out)
        elif isinstance(entity, Room):
            self.retrieve_by_room(entity)
        elif isinstance(entity, Customer):
            if out is None:
                out = entity.construction.address.address1
            for room in entity.rooms:
                self.retrieve_by_room(room)
        for form_handler in self.multi_handlers.values():
            form_handler.create(self.stamp)
            self.files.append(form_handler.path)
        if len(self.files) > 1:
            combined = combine_pdfs(self.files,
                                    os.path.join(self.path,
                                                 self.create_unique_path(out)))
        elif len(self.files) == 1:
            combined = self.files[0]
        else:
            raise my_exceptions.MyBaseException(
                message=
                'Ingen skjemaer å fylle ut. Du må legge til minst en varmekabel/matte.',
                defcon_level=my_exceptions.DefconLevel.warning,
                status_code=403)
        self.file = os.path.relpath(combined)

    def create_unique_path(self, filename, extension='pdf'):
        """Create a path for form, make sure file does not already exist."""
        if filename is None:
            filename = 'noname'
        remove_punctuation_map = dict((ord(char), '-')
                                      for char in string.punctuation)
        slugged = filename.translate(remove_punctuation_map)
        slugged = slugged[:60] if len(slugged) > 60 else slugged
        path = os.path.join(self.path, '{}.{}'.format(slugged, extension))
        i = 2
        while os.path.isfile(path):
            path = os.path.join(self.path, '{}({}).{}'.format(
                slugged, i, extension))
            i += 1
        return path

    def create_path(self, room_item_modification, filename=None):
        """Create a filename from room_item_modification."""
        if not filename:
            filename = " ".join([
                room_item_modification.room_item.room.name,
                room_item_modification.product.name
            ])
        return self.create_unique_path(filename)

    def create_form(self, room_item_modification, filename=None):
        """Create forms, and return a json-object with the url."""
        path = self.create_path(room_item_modification, filename)

        form_handler = FormHandler(
            room_item_modification=room_item_modification,
            current_user=self.user,
            path=path,
            create_if_archived=self.create_if_archived)
        form_handler.create(self.stamp)
        self.files.append(form_handler.path)

    def create_form_multi(self,
                          room_item_modification,
                          manufacturor,
                          filename=None):
        """Create forms, for manufacturors which combine multiple room_items on a signle pdf."""
        path = self.create_path(room_item_modification, filename)
        if manufacturor in self.multi_handlers:
            form_handler = self.multi_handlers[manufacturor]

            form_handler._count += 1
            form_handler.populate(room_item_modification)
        else:
            form_handler = FormHandler(
                room_item_modification=room_item_modification,
                current_user=self.user,
                path=path,
                create_if_archived=self.create_if_archived)
            self.multi_handlers[manufacturor] = form_handler

    def retrieve_by_room_item(self, room_item, filename=None):
        """Retrieve pdf-form by room_item."""
        if not room_item:
            raise my_exceptions.NotARoomItem()
        room_item_modification = room_item.latest
        if not room_item_modification:
            raise my_exceptions.NotARoomItemModification()
        if self.create_if_archived or not room_item_modification.is_archived:
            manufacturor = room_item_modification.product.product_type.manufacturor.name
            if manufacturor == 'Thermofloor':
                self.create_form_multi(room_item_modification, manufacturor,
                                       filename)
            else:
                self.create_form(room_item_modification, filename)

    def retrieve_by_room(self, room):
        """Return pdf-forms by room, recursively."""
        if not room:
            raise my_exceptions.NotARoom()
        for room_item in room.items:
            self.retrieve_by_room_item(room_item)


class FormHandler(object):
    """Push data from model to form-creator."""

    def __init__(self,
                 room_item_modification,
                 current_user,
                 path,
                 create_if_archived=False):
        if not create_if_archived and room_item_modification.is_archived:
            raise ValueError(
                ('Got an arhcived item. If you want to create this pdf anyway, '
                 'set the "create_if_archived" to True"'))
        self.room_item_modification = room_item_modification
        self.product = room_item_modification.product
        self.current_user = current_user
        self.dictionary = {}
        self._count = 0
        self._unique_count = 0
        self.populate(self.room_item_modification)
        self.path = path
        self.url = os.path.relpath(path)
        self.push_from_company(current_user.company)

    @property
    def subfix(self):
        """Subfix used where mulgiple room_items on save pdf."""
        return '' if self._count == 0 else str(self._count + 1)

    @property
    def unique_subfix(self):
        """Subfix used where mulgiple room_items on save pdf."""
        return '_2' if self._unique_count == 0 else str(self._unique_count +
                                                        1) + '_2'

    def populate(self, room_item_modification):
        """Populate dictionary for filling pdf-form."""
        room = room_item_modification.room_item.room
        self.push_from_customer(room.customer)
        self.push_from_product(room_item_modification.product)
        self.push_from_room(room)
        self.push_from_room(room, unique=True)
        self.calculate_room_totals(room_item_modification)
        self.push_from_room_item_modification(room_item_modification)

    def push_from_company(self, company):
        """Push data from company."""
        company_data = {
            'company.name':
                company.name,
            'company.orgnumber':
                company.orgnumber,
            'company.orgnumber_f':
                NumberFormatter.org(company.orgnumber),
            'company.address.address1':
                company.address.address1,
            'company.address.address2':
                company.address.address2,
            'company.address.post_code':
                company.address.post_code,
            'company.address.post_area':
                company.address.post_area,
            'company.contact_name':
                company.contact_name,
            'company.contact_phone':
                company.contact_phone,
            'company.contact_phone_f':
                NumberFormatter.phone(company.contact_phone),
            'company.contact_email':
                company.contact_email,
        }
        self.dictionary.update(company_data)

    def push_from_customer(self, customer):
        """Push data from customer."""
        self.dictionary.update({
            'customer.customer_name':
                customer.construction.customer_name,
            'customer.address.address1':
                customer.construction.address.address1,
            'customer.address.address2':
                customer.construction.address.address2,
            'customer.address.post_area':
                customer.construction.address.post_area,
            'customer.address.post_code':
                customer.construction.address.post_code,
            'customer.contact_name':
                customer.construction.contact_name,
            'customer.phone':
                customer.construction.phone,
            'customer.mobile':
                customer.construction.mobile,
            'customer.phone_f':
                NumberFormatter.phone(customer.construction.phone),
            'customer.mobile_f':
                NumberFormatter.mobile(customer.construction.mobile),
            'customer.orgnumber':
                customer.construction.orgnumber,
            'customer.orgnumber_f':
                NumberFormatter.org(customer.construction.orgnumber),
            'customer.construction_new':
                customer.construction_new,
            'customer.construction_voltage':
                customer.construction_voltage,
        })
        if customer.owner:
            self.dictionary.update({
                'customer.owner.customer_name':
                    customer.owner.customer_name,
                'customer.owner.address.address1':
                    customer.owner.address.address1,
                'customer.owner.address.address2':
                    customer.owner.address.address2,
                'customer.owner.address.post_area':
                    customer.owner.address.post_area,
                'customer.owner.address.post_code':
                    customer.owner.address.post_code,
                'customer.owner.contact_name':
                    customer.owner.contact_name,
                'customer.owner.phone':
                    customer.owner.phone,
                'customer.owner.phone_f':
                    NumberFormatter.phone(customer.owner.phone),
                'customer.owner.mobile_f':
                    NumberFormatter.mobile(customer.owner.mobile),
                'customer.owner.mobile':
                    customer.owner.mobile,
                'customer.owner.orgnumber':
                    customer.owner.orgnumber,
                'customer.owner.orgnumber_f':
                    NumberFormatter.org(customer.owner.orgnumber),
            })

    def push_from_product(self, product):
        """Push data from product."""
        calc = OhmsLaw(
            voltage=product.product_type.secondarySpec,
            resistance=product.resistance_nominal)
        self.dictionary.update({
            'product.effect' + self.subfix:
                product.effect,
            'product.watt_per_(square)_meter' + self.subfix:
                product.product_type.mainSpec,
            'product.voltage' + self.subfix:
                calc.voltage,
            'product.current' + self.subfix:
                calc.current,
            'product.product_type.name' + self.subfix:
                product.product_type.name,
            'product.name' + self.subfix:
                product.name,
            'product.resistance_max' + self.subfix:
                product.resistance_max,
            'product.resistance_min' + self.subfix:
                product.resistance_min,
            'product.resistance_nominal' + self.subfix:
                calc.resistance,
            'product.twowires' + self.subfix: (
                True if product.product_type.catagory not in [
                    ProductCatagory.single_inside,
                    ProductCatagory.single_outside
                ] else False)
        })

    def push_from_room(self, room, unique=False):
        """
        Push data from room.

        Unique should only be set to true if this pdf can contain multiple
        rooms, and the rooms should only be listed uniquely.
        """
        last_room_name = None
        subfix = self.subfix
        if unique:
            subfix = self.unique_subfix
            last_room_name = self.dictionary.get('room.name{}'.format(subfix))
            if last_room_name and last_room_name != room.name:
                self._unique_count += 1
                subfix = self.unique_subfix
        if last_room_name != room.name:
            self.dictionary.update({
                'room.name' + subfix:
                    room.name,
                'room.area' + subfix:
                    room.area,
                'room.heated_area' + subfix:
                    room.heated_area,
                'room.product_count' + subfix:
                    len(room.items),
                'earthed_cable_screen' + subfix:
                    room.earthed_cable_screen,
                'earthed_chicken_wire' + subfix:
                    room.earthed_chicken_wire,
                'earthed_other' + subfix:
                    room.earthed_other,
                'max_temp_planning' + subfix:
                    room.max_temp_planning,
                'max_temp_installation' + subfix:
                    room.max_temp_installation,
                'max_temp_other' + subfix:
                    room.max_temp_other,
                'control_system_floor_sensor' + subfix:
                    room.control_system_floor_sensor,
                'control_system_room_sensor' + subfix:
                    room.control_system_room_sensor,
                'control_system_limit_sensor' + subfix:
                    room.control_system_limit_sensor,
                'control_system_designation' + subfix:
                    room.control_system_designation,
                'control_system_other' + subfix:
                    room.control_system_other,
                'installation_depth' + subfix:
                    room.installation_depth,
                'ground_fault_protection' + subfix:
                    room.ground_fault_protection,
                'curcuit_breaker_size' + subfix:
                    room.curcuit_breaker_size,
                'handed_to_owner' + subfix:
                    room.handed_to_owner,
                'owner_informed' + subfix:
                    room.owner_informed,
            })
            if not room.outside and room.inside_specs:
                self.dictionary.update(
                    room.inside_specs.serialize('inside_specs.'))
            if room.outside and room.outside_specs:
                self.dictionary.update(
                    room.outside_specs.serialize('outside_specs.'))

    def calculate_room_totals(self, room_item_modification):
        """For multiple room_items on same pdf, calculate totals."""

        def retrieve_key(key):
            """Retrieve a key from measurements on a room_item_modification."""
            value = 0
            try:
                value = float(room_item_modification.specs['measurements'][
                    'install'][key])
            except (AttributeError, KeyError, ValueError, TypeError):  #
                pass
            return value

        subfix = self.unique_subfix
        ohm = retrieve_key('ohm')
        mohm = retrieve_key('mohm')
        if ohm > 0:
            key = 'install{}.ohm'.format(subfix)
            I_key = 'install{}.I'.format(subfix)
            old_ohm = float(self.dictionary.get(key, 0))
            calc = OhmsLaw(
                voltage=room_item_modification.product.product_type.
                secondarySpec,
                resistance=[ohm, old_ohm])
            self.dictionary.update({key: calc.resistance})
            try:
                self.dictionary.update({I_key: calc.current})
            except ValueError:
                pass
        if mohm > 0:
            new_mohm = mohm
            key = 'install{}.mohm'.format(subfix)
            old_mohm = self.dictionary.get(key, 999999)
            self.dictionary.update({key: min(old_mohm, new_mohm)})

    def push_from_room_item_modification(self, room_item_modification):
        """Push data from room_item_modification."""

        specs = room_item_modification.specs.copy()
        self.dictionary.update({
            'installed_by' + self.subfix:
                '{} {}'.format(room_item_modification.user.given_name,
                               room_item_modification.user.family_name)
        })

        if specs: # noqa
            for key in [
                    'area_output', 'cc', 'installation_depth',
                    'curcuit_breaker_size'
            ]:
                if key in specs:
                    variable = specs[key]['v']
                    if variable:
                        self.dictionary.update({
                            key + self.subfix: variable,
                        })
            if 'measurements' in specs:
                m = specs['measurements'].copy()
                n = {}
                last_date = None
                for key, value in m.items():
                    if isinstance(value, dict):
                        date = value.get('date')
                        if date:
                            parsed = parse(date)
                            if not last_date or parsed > last_date:
                                last_date = parsed
                            m[key]['date'] = parsed
                            ohm = m[key].get('ohm')
                            if ohm and room_item_modification.product:
                                calc = OhmsLaw(
                                    resistance=ohm,
                                    voltage=room_item_modification.product.
                                    product_type.secondarySpec)
                                m[key]['I'] = calc.current
                            n[key + self.subfix] = m[key]
                if last_date:
                    n['last_date' + self.subfix] = last_date

                self.dictionary.update(flatten_dict(n))

    def stamp_with_user(self, user, form):
        """Description."""
        if user.signature:
            image = os.path.join(os.path.split(self.path)[0], 'sign.png')
            with open(image, 'wb') as f:
                f.write(user.signature)
            stamped_pdf = form.stamp_with_image(self.path, image, 20, 10)
            os.remove(image)
            os.remove(self.path)
            os.rename(stamped_pdf, self.path)

    def create(self, stamp=False):
        """Create a form."""
        # form = FormField(
        #     self.product.product_type.manufacturor.name, self.dictionary)
        form = get_template_schema(
            manufacturor=self.product.product_type.manufacturor.name,
            dictionary=self.dictionary)
        complete_dictionary = form.create_filled_pdf(self.path)
        if stamp:
            self.stamp_with_user(self.current_user, form)
        return complete_dictionary
