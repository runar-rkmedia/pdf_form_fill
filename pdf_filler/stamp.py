import os
from subprocess import check_output
import struct
import imghdr
from .pdf_form import PdfForm


def signatere_location_size(x, y, w, h):
    return {
        'x': x,
        'y': y,
        'w': w,
        'h': h
    }


class Stamp(object):

    def __init__(self, signature_location_sizes):
        self.signature_location_sizes = signature_location_sizes

    def stamp_with_image(self, output_path, image, offsetx, offsety, page=1):
        """Will put image on top of this pdf using java"""
        # TODO: should go back to imagemagick
        image_size = self.get_image_size(image)
        import warnings
        warnings.warn(
            "Use imagemagick and vectorgraphics instead of java-stamp",
            DeprecationWarning)
        for signature_location_size in self.signature_location_sizes:
            dpi = max(
                image_size[0] * 72 / signature_location_size['w'],
                image_size[1] * 72 / signature_location_size['h']
            )
            call = [
                'java',
                '-jar',
                'pdfstamp/pdfstamp.jar',
                '-i',
                image,
                '-d',
                str(int(dpi)),
                '-l',
                "{},{}".format(
                    signature_location_size['x'],
                    signature_location_size['y']
                ),
                '-p',
                str(signature_location_size.get('p', 1)),
                '-e',
                's',
                output_path]
            check_output(call).decode('utf8')
            path, filename = os.path.split(output_path)
            filename, ext = os.path.splitext(filename)
            newfilename = '{}_s{}'.format(filename, ext)
            output_path = os.path.join(path, newfilename)
        return output_path

    def get_image_size(self, fname):
        '''Determine the image type of fhandle and return its size.
        from draco'''
        with open(fname, 'rb') as fhandle:
            head = fhandle.read(24)
            if len(head) != 24:
                return
            if imghdr.what(fname) == 'png':
                check = struct.unpack('>i', head[4:8])[0]
                if check != 0x0d0a1a0a:
                    return
                width, height = struct.unpack('>ii', head[16:24])
            elif imghdr.what(fname) == 'gif':
                width, height = struct.unpack('<HH', head[6:10])
            elif imghdr.what(fname) == 'jpeg':
                try:
                    fhandle.seek(0)  # Read 0xff next
                    size = 2
                    ftype = 0
                    while not 0xc0 <= ftype <= 0xcf:
                        fhandle.seek(size, 1)
                        byte = fhandle.read(1)
                        while ord(byte) == 0xff:
                            byte = fhandle.read(1)
                        ftype = ord(byte)
                        size = struct.unpack('>H', fhandle.read(2))[0] - 2
                    # We are at a SOFn block
                    fhandle.seek(1, 1)  # Skip `precision' byte.
                    height, width = struct.unpack('>HH', fhandle.read(4))
                except Exception:  # IGNORE: W0703
                    return
            else:
                return
            return width, height


class StampablePdfForm(PdfForm, Stamp):

    def __init__(
            self,
            dictionary,
            fill_pdf_filename,
            fields_dict,
            checkbox_value,
            signature_location_sizes
    ):
        PdfForm.__init__(
            self,
            dictionary=dictionary,
            fill_pdf_filename=fill_pdf_filename,
            fields_dict=fields_dict,
            checkbox_value=checkbox_value
        )

        Stamp.__init__(
            self,
            signature_location_sizes=signature_location_sizes
        )
