"""Create forms from database-objects."""

import os
import string

import my_exceptions
from dateutil.parser import parse
from models_credentials import ContactType, Customer, Room, RoomItem
from models_product import ProductCatagory
from pdf_filler.helpers import NumberFormatter
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

    def __init__(self, entity, user, stamp=None, out=None, create_if_archived=False):
        self.path = user_file_path(create_random_dir=True)
        self.create_if_archived = create_if_archived
        self.files = []
        self.user = user
        self.stamp = stamp
        if isinstance(entity, RoomItem):
            self.retrieve_by_room_item(entity, out)
        elif isinstance(entity, Room):
            self.retrieve_by_room(entity)
        elif isinstance(entity, Customer):
            if out is None:
                out = entity.address.address1
            for room in entity.rooms:
                self.retrieve_by_room(room)
        if len(self.files) > 1:
            combined = combine_pdfs(
                self.files,
                os.path.join(self.path, self.create_unique_path(out)))
        elif len(self.files) == 1:
            combined = self.files[0]
        else:
            raise my_exceptions.MyBaseException(
                message='Ingen skjemaer å fylle ut. Du må legge til minst en varmekabel/matte.',
                defcon_level=my_exceptions.DefconLevel.warning,
                status_code=403
            )
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
            path = os.path.join(self.path, '{}({}).{}'.format(slugged, i, extension))
            i += 1
        return path

    def create_form(self, room_item_modification, filename=None):
        """Create forms, and return a json-object with the url."""
        if not filename:
            filename = " ".join([
                room_item_modification.room_item.room.name,
                room_item_modification.product.name
            ])
        path = self.create_unique_path(filename)

        form_handler = FormHandler(
            room_item_modification=room_item_modification,
            current_user=self.user,
            path=path,
            create_if_archived=self.create_if_archived)
        form_handler.create(self.stamp)
        return form_handler.path

    def retrieve_by_room_item(self, room_item, filename=None):
        """Retrieve pdf-form by room_item."""
        if not room_item:
            raise my_exceptions.NotARoomItem()
        room_item_modification = room_item.latest
        if not room_item_modification:
            raise my_exceptions.NotARoomItemModification()
        if self.create_if_archived or not room_item_modification.is_archived:
            f = self.create_form(room_item_modification, filename)
            self.files.append(f)

    def retrieve_by_room(self, room):
        """Return pdf-forms by room, recursively."""
        if not room:
            raise my_exceptions.NotARoom()
        for room_item in room.items:
            self.retrieve_by_room_item(room_item)


class FormHandler(object):
    """Push data from model to form-creator."""

    def __init__(self, room_item_modification, current_user, path, create_if_archived=False):
        if not create_if_archived and room_item_modification.is_archived:
            raise ValueError((
                'Got an arhcived item. If you want to create this pdf anyway, '
                'set the "create_if_archived" to True"'
            ))
        self.room_item_modification = room_item_modification
        self.current_user = current_user
        self.dictionary = {}
        # Set up some shortcut to objects used
        self.room = room_item_modification.room_item.room
        self.customer = self.room.customer
        self.company = self.customer.company
        self.product = room_item_modification.product
        self.populate()
        self.path = path
        self.url = os.path.relpath(path)

    def populate(self):
        """Populate dictionary for filling pdf-form."""
        self.push_from_company()
        self.push_from_customer()
        self.push_from_product()
        self.push_from_room()
        self.push_from_room_item_modification()

    def push_from_company(self):
        """Push data from company."""
        company_data = {
            'company.name': self.company.name,
            'company.orgnumber': self.company.orgnumber,
            'company.orgnumber_f': NumberFormatter.org(self.company.orgnumber),
            'company.address.address1': self.company.address.address1,
            'company.address.address2': self.company.address.address2,
            'company.address.post_code': self.company.address.post_code,
            'company.address.post_area': self.company.address.post_area,
        }
        for contact in self.company.contacts:
            if contact.contact.type == ContactType.email:
                company_data['company.contact.email'] = contact.contact.value
            if contact.contact.type == ContactType.phone:
                company_data['company.contact.phone'] = contact.contact.value
                company_data['company.contact.phone_f'] = NumberFormatter.phone(
                    contact.contact.value)
            if contact.contact.type == ContactType.mobile:
                company_data['company.contact.mobile'] = contact.contact.value
                company_data['company.contact.mobile_f'] = NumberFormatter.mobile(
                    contact.contact.value)
            if contact.contact.description:
                company_data[
                    'company.contact.person'] = contact.contact.description
        self.dictionary.update(company_data)

    def push_from_customer(self):
        """Push data from customer."""
        self.dictionary.update({
            'kunde_navn': self.customer.name,
            'customer.address.address1': self.customer.address.address1,
            'customer.address.address2': self.customer.address.address2,
            'customer.address.post_area': self.customer.address.post_area,
            'customer.address.post_code': self.customer.address.post_code
        })

    def push_from_product(self):
        """Push data from product."""
        self.dictionary.update({
            'product.effect': self.product.effect,
            'product.watt_per_(square)_meter':
            self.product.product_type.mainSpec,
            'product.voltage':
            self.product.product_type.secondarySpec,
            'product.product_type.name': self.product.product_type.name,
            'product.name': self.product.name,
            'product.resistance_max': self.product.resistance_max,
            'product.resistance_min': self.product.resistance_min,
            'product.resistance_nominal': self.product.resistance_nominal,
            'product.twowires': (
                True
                if self.product.product_type.catagory not in [
                    ProductCatagory.single_inside,
                    ProductCatagory.single_outside]
                else
                False
            )
        })

    def push_from_room(self):
        """Push data from room."""
        self.dictionary.update({
            'room.name': self.room.name,
            'room.area': self.room.area,
            'room.heated_area': self.room.heated_area,
            'room.product_count': len(self.room.items),
            'earthed_cable_screen': self.room.earthed_cable_screen,
            'earthed_chicken_wire': self.room.earthed_chicken_wire,
            'earthed_other': self.room.earthed_other,
            'max_temp_planning': self.room.max_temp_planning,
            'max_temp_installation': self.room.max_temp_installation,
            'max_temp_other': self.room.max_temp_other,
            'control_system_floor_sensor': self.room.control_system_floor_sensor,
            'control_system_room_sensor': self.room.control_system_room_sensor,
            'control_system_designation': self.room.control_system_designation,
            'control_system_other': self.room.control_system_other,
            'installation_depth': self.room.installation_depth,
            'ground_fault_protection': self.room.ground_fault_protection,
            'curcuit_breaker_size': self.room.curcuit_breaker_size,
        })

    def push_from_room_item_modification(self):
        """Push data from room_item_modification."""
        specs = self.room_item_modification.specs.copy()

        if specs:
            for key in [
                    'area_output',
                    'cc',
                    'installation_depth',
                    'curcuit_breaker_size'
            ]:
                if key in specs:
                    variable = specs[key]['v']
                    if variable:
                        self.dictionary.update({
                            key: variable,
                        })
            if 'measurements' in specs:
                m = specs['measurements'].copy()
                n = {}
                for key, value in m.items():
                    if isinstance(value, dict):
                        date = value.get('date')
                        if date:
                            m[key]['date'] = parse(date)
                            n[key] = m[key]
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
