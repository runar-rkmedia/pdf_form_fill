"""part of smart pdf filler."""
from time import gmtime, strftime
import string
import random
NumberTypes = (int, float, complex)


def currentDate(date_format="%d.%m.%Y"):
    """Get formated current date."""
    return strftime(date_format, gmtime())


def commafloat(string_as_number):
    """Return a float from string with comma as decimal-seperator."""
    return float(string_as_number.replace(',', '.'))


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """Return random string with digits."""
    return ''.join(random.choice(chars) for _ in range(size))


def group_number(n, grouping=3, seperator=' '):
    """Returns a pretty, grouped number."""
    # 10x performance
    if grouping == 3:
        s = format(n, ',')
        if seperator == ',':
            return s
        return s.replace(',', seperator)
    # Slow, general grouping
    else:
        r = []
        for i, c in enumerate(reversed(str(n))):
            if i and (not (i % grouping)):
                r.insert(0, seperator)
            r.insert(0, c)
        return ''.join(r)


def get_image_size(fname):
    '''Determine the image type of fhandle and return its size.
    from draco'''
    import struct
    import imghdr
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
            except Exception:  # IGNORE:W0703
                return
        else:
            return
        return width, height
