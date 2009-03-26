import os.path

from fiftyfive.apps.imgtool.helpers.ImageMagick import resize, resize_and_crop

from fiftyfive.apps.imgtool.helpers.utils_base import _generateProxyName, _generateProxyURL
from fiftyfive.apps.imgtool.helpers.utils_base import _getImageDimension

# Magic
def parameters(only=None, exclude=None, ignore='self'):
    """
    Returns a dictionary of the calling functions 
    parameter names and values.

    The optional arguments can be used to filter the result:

       only           use this to only return parameters 
                      from this list of names.

       exclude        use this to return every parameter 
                      *except* those included in this list
                      of names.

       ignore         use this inside methods to ignore 
                      the calling object's name. For 
                      convenience, it ignores 'self' 
                      by default.
    """
    import inspect
    args, varargs, varkw, defaults = \
        inspect.getargvalues(inspect.stack()[1][0])
    if only is None:
        only = args[:]
        if varkw:
            only.extend(defaults[varkw].keys())
            defaults.update(defaults[varkw])
    if exclude is None:
        exclude = []
    exclude.append(ignore)
    return dict([(attrname, defaults[attrname])
        for attrname in only if attrname not in exclude])

class Image(object):
    def __init__(self,
        url, filename, width=0, height=0):
        self.__dict__.update( parameters() )
        self._setImageInfo()
        self.ratio = float(self.width)/self.height

    def _setImageInfo(self):
        self.width, self.height = map(int, (self.width, self.height))
        if (self.width <= 0)  or (self.height <= 0):
            self.width, self.height = _getImageDimension(self.filename)

        self.format = os.path.splitext(self.filename)[1][1:].lower()

class ImageProxy(object):
    def __init__(self,
        img=Image, format=None,
        rq_width=0, rq_height=0,
        crop=False, density=False,
        root=None, url_root=None):

        if crop:
            assert (rq_width > 0) and (rq_height > 0) # both h/w must be supplied if crop=True

        # If format is specified and no w/h set, then assume the same dimension
        # as master. Otherwise set the format to be the same as master.
        if format != None:
            format = format.lower()
            if (rq_width == 0) and (rq_height == 0):
                rq_width, rq_height = img.width, img.height
        else:
            format = img.format

        # Make sure w/h are not negative numbers and
        # one of width/height is required
        assert ((rq_width >= 0) and (rq_height >= 0))
        assert (type(rq_width) == int) and (type(rq_height) == int) # make sure w/h are integers

        self.__dict__.update( parameters() ) # Use the magic to initialize instance variables

    def generate(self):
        """
        Generates the actual proxy.
        """
        # If file already exists
        if os.path.isfile(self.filename) \
        and not (os.path.getmtime(self.img.filename) > os.path.getmtime(self.filename)):
            pass
        else: # If exit_status of convert() is anything other than 0 (success)
            if self.crop:
                status = resize_and_crop(self.img.filename, self.filename,
                                         self.width_convert, self.height_convert,
                                         self.width, self.height,
                                         self.x_offset, self.y_offset, self.density)
            else:
                status = resize(self.img.filename, self.filename,
                                self.width_convert, self.height_convert, self.density)
            if status:
                # this goes to webserver error log
                import sys
                print >>sys.stderr, '[MAKE THUMBNAIL] error for file %r' % (self.filename)
                raise RuntimeError

    def _calcHelper(self, int1, int2, int3):
        """
        Helper method that returns:
        int( round( int1 * ( float(int2) / int3 )))
        """
        return int( round( int1 * ( float(int2) / int3 )))

    # Properties definition
    def _calculateImageInfo(self):
        """
        Helper method to calculate a bunch of information
        about the proxy: width, height, ratio, etc.
        """
        if self.crop:
            w_ratio = float(self.rq_width) / self.img.width
            h_ratio = float(self.rq_height) / self.img.height
            self._width_convert, self._height_convert = map(
                lambda x:int(x*max(w_ratio, h_ratio)), (self.img.width, self.img.height))
            self._x_offset = int((self._width_convert - self.rq_width) / 2.)
            self._y_offset = int((self._height_convert - self.rq_height) / 2.)
            self._width, self._height = self.rq_width, self.rq_height
        else:
            if (self.rq_ratio == ZeroDivisionError):
                self._width = int(self.rq_width)
                self._height = self._calcHelper(self.img.height, self.rq_width, self.img.width)
            elif (self.rq_ratio == 0) or (self.img.ratio < self.rq_ratio):
                self._width = self._calcHelper(self.img.width, self.rq_height, self.img.height)
                self._height = int(self.rq_height)
            elif (self.img.ratio >= self.rq_ratio):
                self._width = int(self.rq_width)
                self._height = self._calcHelper(self.img.height, self.rq_width, self.img.width)
            else:
                raise AttributeError

            self._width_convert, self._height_convert = self._width, self._height
            self._x_offset = self._y_offset = 0

    def getRqRatio(self):
        """
        0.0 would mean only height was specified.
        ZeroDivisionError would mean only width was specified.
        Any other number would mean both are specified.
        """
        try:
            return float(self.rq_width)/self.rq_height
        except ZeroDivisionError:
            return ZeroDivisionError

    def _isProxySameAsMater(self):
        # If it's the same size and format as the master, return True
        if (self.width == self.img.width) \
        and (self.height == self.img.height) \
        and (self.format.lower() == self.img.format):
            return True
        else:
            return False


    def getFilename(self):
        try:
            return self._filename
        except:
            # If it's the same size and format as the master, just return the master
            if self._isProxySameAsMater():
                self._filename = os.path.normpath(self.img.filename)
            else:
                self._filename = _generateProxyName(
                    self.img.filename, self.width, self.height, self.format, self.density)
            return self._filename

    def getFileURL(self):
        try:
            return self._url
        except:
            # If it's the same size and format as the master, just return the master
            if self._isProxySameAsMater():
                self._url = self.img.url
            else:
                self._url = _generateProxyURL(
                    self.img.url, self.width, self.height, self.format, self.density)
            return self._url

    def _genericGetter(self, attr):
        try:
            return getattr(self, attr)
        except:
            self._calculateImageInfo()
            return getattr(self, attr)

    def getWidth(self):
        return self._genericGetter('_width')

    def getHeight(self):
        return self._genericGetter('_height')

    def getWidthConvert(self):
        return self._genericGetter('_width_convert')

    def getHeightConvert(self):
        return self._genericGetter('_height_convert')

    def getXOffset(self):
        return self._genericGetter('_x_offset')

    def getYOffset(self):
        return self._genericGetter('_y_offset')

    rq_ratio = property(getRqRatio, doc="Aspect ratio of request.")
    width = property(getWidth, doc="Calculated width for proxy.")
    height = property(getHeight, doc="Calculated height for proxy.")
    filename = property(getFilename, doc="Filename for the proxy.")
    url = property(getFileURL, doc="URL for the proxy.")
    width_convert = property(getWidthConvert, doc="Conversion width for a cropped proxy")
    height_convert = property(getHeightConvert, doc="Conversion height for a cropped proxy")
    x_offset = property(getXOffset, doc="Specify the location of the upper left corner of the cropping region measured downward and rightward with respect to the upper left corner of the image")
    y_offset = property(getYOffset, doc="Specify the location of the upper left corner of the cropping region measured downward and rightward with respect to the upper left corner of the image")
    