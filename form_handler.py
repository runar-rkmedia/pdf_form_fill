import os
# from models_product import Product
from vk_objects import FormField


class FormHandler(object):
    """Push data from model to form-creator."""

    def __init__(self, room_item_modification, current_user):
        self.entity = room_item_modification
        self.current_user = current_user
        self.dictionary = {}
        # Set up some shortcut to objects used
        self.room = room_item_modification.room_item.room
        self.customer = self.room.customer
        self.company = self.customer.company
        self.product = room_item_modification.product
        self.populate()

    def populate(self):
        """Populate dictionary for filling pdf-form."""
        self.push_from_company()

    def push_from_company(self):
        """Description."""
        d = {}
        d['firma_navn'] = self.company.name
        d['firma_orgnr'] = self.company.orgnumber
        d['firma_adresse1'] = self.company.address.address1
        d['firma_adresse2'] = self.company.address.address2
        d['firma_poststed'] = self.company.address.post_area
        d['firma_postnummer'] = self.company.address.post_code
        self.dictionary.update(d)

    def stamp_with_user(user, output_pdf, form):
        """Description."""
        if user.signature:
            image = os.path.join(os.path.split(output_pdf)[0], 'sign.png')
            with open(image, 'wb') as f:
                f.write(user.signature)
            stamped_pdf = form.stamp_with_image(output_pdf, image, 20, 10)
            os.remove(image)
            os.remove(output_pdf)
            os.rename(stamped_pdf, output_pdf)

    @property
    def url(self):
        """Return url of this object."""
        try:
            return os.path.relpath(self.path)
        except AttributeError:
            raise AttributeError('path not set. ',
                                 'Please set it by running create(path)')

    def create(self, path):
        """Create a form."""
        self.path = path
        form = FormField(self.product.product_type.manufacturor.name)
        form.set_fields_from_dict(self.dictionary)
        complete_dictionary = form.create_filled_pdf(path)
        # stamp_with_user(user, path, form)
        return path, complete_dictionary, form
