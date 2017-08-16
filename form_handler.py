import os
from vk_objects import FormField
from pprint import pprint


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
            'firma_navn': self.company.name,
            'firma_orgnr': self.company.orgnumber,
            'firma_adresse1': self.company.address.address1,
            'firma_adresse2': self.company.address.address2,
            'firma_poststed': self.company.address.post_area,
            'firma_postnummer': self.company.address.post_code
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
            'effect': self.product.product_type.mainSpec,
            'produkt_type': self.product.product_type.name
        })

    def push_from_room(self):
        """Push data from product."""
        self.dictionary.update({
            'rom_navn': self.room.name
        })

    def push_from_room_item_modification(self):
        """Push data from room_item_modification."""
        self.dictionary.update(
            self.room_item_modification.specs['measurements'])
        self.dictionary.update({
            'dato': self.room_item_modification.date
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
        form = FormField(
            self.product.product_type.manufacturor.name, self.dictionary)
        complete_dictionary = form.create_filled_pdf(self.path)
        if stamp:
            self.stamp_with_user(self.current_user, form)
        pprint(self.dictionary)
        pprint(complete_dictionary)
        # TODO: FIX complete_dictionary. it has wrong keys.
        return complete_dictionary
