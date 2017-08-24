import os
from pdf_filler.schema import get_template_schema
from models_product import ProductCatagory


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
            'control_system_other': self.room.control_system_other
        })

    def push_from_room_item_modification(self):
        """Push data from room_item_modification."""
        specs = self.room_item_modification.specs.copy()

        if specs:
            if 'area_output' in specs:
                self.dictionary.update({
                    'area_output': specs['area_output']['v'],
                })
            if 'cc' in specs:
                self.dictionary.update({
                    'cc': specs['cc']['v'],
                })
            if 'measurements' in specs:
                measurements = specs['measurements']
                for key, value in measurements.items():
                    try:
                        if value and int(value) <= 0:
                            measurements[key] = ''
                    except ValueError:
                        pass
                    else:
                        self.dictionary.update(measurements)
                        self.dictionary.update({
                            'date': self.room_item_modification.date
                        })

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
