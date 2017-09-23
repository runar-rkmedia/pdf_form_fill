"""Create forms from database-objects."""

import os

import my_exceptions
from dateutil.parser import parse
from models_credentials import Customer, Room, RoomItem
from models_product import ProductCatagory
from pdf_filler.schema import get_template_schema
from pdffields.fields import combine_pdfs
from setup_app import user_file_path


def flatten_dict(d):
    def items():
        for key, value in d.items():
            if isinstance(value, dict):
                for subkey, subvalue in flatten_dict(value).items():
                    yield key + "." + subkey, subvalue
            else:
                yield key, value

    return dict(items())


class MultiForms(object):
    """Create multiple pdf-forms recursively, depending on input."""

    def __init__(self, entity, user, stamp=True, out='out.pdf'):
        self.path = user_file_path(create_random_dir=True)
        self.files = []
        self.user = user
        self.stamp = stamp
        if isinstance(entity, RoomItem):
            self.retrieve_by_room_item(entity)
        elif isinstance(entity, Room):
            self.retrieve_by_room(entity)
        elif isinstance(entity, Customer):
            for room in entity.rooms:
                self.retrieve_by_room(room)
        combined = combine_pdfs(
            self.files,
            os.path.join(self.path, 'out.pdf'))
        self.file = os.path.relpath(combined)

    def create_path(self, path):
        """Create a path for form."""

    def create_form(self, room_item_modification):
        """Create forms, and return a json-object with the url."""
        filename = " ".join([
            room_item_modification.room_item.room.customer.address.address1,
            room_item_modification.product.name
        ])
        import string
        remove_punctuation_map = dict((ord(char), '-')
                                      for char in string.punctuation)
        slugged = filename.translate(remove_punctuation_map)
        slugged = slugged[:60] if len(slugged) > 60 else slugged

        form_handler = FormHandler(
            room_item_modification,
            self.user, os.path.join(self.path, slugged + '.pdf'))
        form_handler.create(self.stamp)
        return form_handler.path

    def retrieve_by_room_item(self, room_item):
        """Retrieve pdf-form by room_item."""
        if not room_item:
            raise my_exceptions.NotARoomItem()
        if not room_item.latest:
            raise my_exceptions.NotARoomItemModification()
        self.files.append(self.create_form(room_item.latest))

    def retrieve_by_room(self, room):
        """Return pdf-forms by room, recursively."""
        if not room:
            raise my_exceptions.NotARoom()
        for room_item in room.items:
            self.retrieve_by_room_item(room_item)


class FormHandler(object):
    """Push data from model to form-creator."""

    def __init__(self, room_item_modification, current_user, path):
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
        self.dictionary.update({
            'company.name': self.company.name,
            'company.orgnumber': self.company.orgnumber,
            'company.address.address1': self.company.address.address1,
            'company.address.address2': self.company.address.address2,
            'company.address.post_code': self.company.address.post_code,
            'company.address.post_area': self.company.address.post_area,
        })

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
                    if variable and len(variable) > 0:
                        self.dictionary.update({
                            key: variable,
                        })
            if 'measurements' in specs:
                m = specs['measurements'].copy()
                for key, value in m.items():  # noqa
                    if isinstance(m[key], dict):
                        date = m[key].get('date')
                        if date:
                            m[key]['date'] = parse(date)
                self.dictionary.update(flatten_dict(m))

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
