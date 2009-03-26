import os.path

from django.conf import settings
from fiftyfive.apps.imgtool.classes.Image import ImageProxy

from fiftyfive.apps.imgtool.helpers.utils_base import _removeProxies
from fiftyfive.apps.imgtool.helpers.utils_base import HAS_PIL

def makeProxy(img_obj, format=None, width=0, height=0, crop=False, density=False,
              root=settings.MEDIA_ROOT, url_root=settings.MEDIA_URL):
    """
    Create a proxy if one doesn't exist on the filesystem already.
    Returns the URL of the resulting proxy. If the requested size is
    the same as photo_url, then photo_url is returned.
    Width and height are bounding boxes, proxies will be generated
    proportionally within that bounding box.
    If crop=True, then width and height act as crop boundaries.
    """

    assert ((width > 0) or (height > 0)) or (format != None) # one of width/height is required, or format
    
    if not HAS_PIL: return None # no PIL - no proxy
    if not img_obj: return None

    proxy = ImageProxy(img_obj, format, width, height, crop, density, root, url_root)
    # Let's make the actual proxy
    try:
        proxy.generate()
        return proxy
    # Specify Error type?
    except:
        # this goes to webserver error log
        import sys
        print >>sys.stderr, '[MAKE PROXY] problem for file %r' % img_obj.filename
        return img_obj
    
def remove_model_proxies(model):
    """ remove all proxies for all ImageFields (and subclasses) in the model """
    from django.db import models
    for field in model._meta.fields:
        if isinstance(field, models.ImageField):
            img_fn = getattr(model, 'get_%s_filename' % field.name)()
            _removeProxies(img_fn)