import os, fnmatch
from urlparse import urljoin
from urllib import pathname2url

from django.conf import settings
from django.core.cache import get_cache
  
image_cache = get_cache('locmem:///')

_FILE_CACHE_TIMEOUT = 60 * 60 * 60 * 24 * 31 # 1 month

try:
    import Image # check for PIL
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


#******************************
# Filename manipulation helpers
#******************************
def _getFilenameParts(path):
    """
    Takes a filename and returns three parts:
    basedir (the path)
    basename (the name of the file w/o extension)
    ext (the file extension, no '.')
    """
    if os.path.isfile:
        basedir = os.path.normpath( os.path.dirname(path) )
        basename, ext = os.path.splitext(os.path.basename(path))
        return basedir, basename, ext
    else:
        raise TypeError

def _changeRoot(path, root=settings.MEDIA_ROOT, new_root=settings.MEDIA_ROOT):
    """Swap out root with new_root for path."""
    root, new_root = map(os.path.normpath, (root, new_root))
    if root != new_root:
        return path.replace(root, new_root)
    else:
        return path


#**************
# Proxy helpers
#**************
def _generateProxyParts(img_path, width=None, height=None, format='jpg', density=False,
    root=settings.MEDIA_ROOT, new_root=settings.MEDIA_ROOT):
    """Helper function for _generateProxyName and _generateProxyURL."""
    assert width and height
    basedir, basename, ext = _getFilenameParts(img_path)
    basedir = _changeRoot(basedir, root, new_root) #Swap out if there's a new_root
    if density:
        proxyname = settings.PROXY_GLOB %( basename, width, height, str(density)+'.'+format )
    else:
        proxyname = settings.PROXY_GLOB %( basename, width, height, 'o.'+format )
    return basedir, proxyname

def _generateProxyName(img_path, width=None, height=None, format='jpg', density=False,
    root=settings.MEDIA_ROOT, new_root=settings.MEDIA_ROOT):
    """Returns the proxy filename, based on the input filename."""
    basedir, proxyname = _generateProxyParts(img_path, width, height, format, density, root, new_root)
    basedir = os.path.join(basedir, settings.PROXY_RELATIVE_PATH)
    return os.path.join( basedir, proxyname )

def _generateProxyURL(img_url, width=None, height=None, format='jpg', density=False,
    root=settings.MEDIA_URL, new_root=settings.MEDIA_URL):
    """Returns the proxy url, based on the input url."""
    basedir, proxyname = _generateProxyParts(img_url, width, height, format, density, root, new_root)
    basedir = pathname2url( os.path.join(basedir, settings.PROXY_RELATIVE_PATH) ) + '/'
    return urljoin( basedir, proxyname )

def _removeProxies(img_path, root=settings.MEDIA_ROOT, new_root=settings.MEDIA_ROOT):
    """Remove the proxies associated with the input_path."""
    basedir, base, ext = _getFilenameParts(img_path)
    proxy_dir = os.path.dirname(_generateProxyName(img_path, 1, 1, 'jpg', root, new_root)) # Use dummy w/h

    try:
        for file in fnmatch.filter(os.listdir(proxy_dir), settings.PROXY_GLOB % (base, '*', '*')):
            path = os.path.join(proxy_dir, file)
            os.remove(path)
            image_cache.delete(path) # delete from cache
    except:
        pass

#***************
# Cache handling
#***************
def _setCachedFile(path, value):
    """
    Store file dependent data in cache.
    Timeout is set to _FILE_CACHE_TIMEOUT (1month).
    """
    
    mtime = os.path.getmtime(path)
    image_cache.set(path, (mtime, value,), _FILE_CACHE_TIMEOUT)

def _getCachedFile(path, default=None):
    """
    Get file content from cache.
    If modification time differ return None and delete
    data from cache, and proxies from filesystem.
    """
    cached = image_cache.get(path, default)

    if cached is None:
        return None

    mtime, value = cached
    if (not os.path.isfile(path)) or (os.path.getmtime(path) != mtime): # file is changed or deleted
        # remove proxies if exists
        _removeThumbnails(path)
        return None
    else:
        return value


#***********
# Image info
#***********
def _noPilImageSize(fname):
    """
    Determine the image type of FNAME and return its size.
    Returns tuple (width, height) or None
    """
    
    try:
        filehandle = file(fname, 'rb')
    except IOError:
        return None

    head = filehandle.read(24)
    if len(head) != 24:
        return
    if head[:4] == '\x89PNG': #PNG
        check = struct.unpack('>i', head[4:8])[0]
        if check != 0x0d0a1a0a:
            return
        width, height = struct.unpack('>ii', head[16:24])
    elif head[:6] in ('GIF87a', 'GIF89a'): #GIF
        width, height = struct.unpack('<HH', head[6:10])
    elif head[:4] == '\xff\xd8\xff\xe0' and head[6:10] == 'JFIF': #JPEG
        filehandle.seek(0)  # Read 0xff next
        size = 2
        filetype = 0
        while not 0xc0 <= filetype <= 0xcf:
            filehandle.seek(size, 1)
            byte = filehandle.read(1)
            while ord(byte) == 0xff:
                byte = filehandle.read(1)
            filetype = ord(byte)
            size = struct.unpack('>H', filehandle.read(2))[0] - 2
        # We are at a SOFn block
        filehandle.seek(1, 1)  # Skip `precision' byte.
        height, width = struct.unpack('>HH', filehandle.read(4))
    else:
        return
    return width, height

def _getImageDimension(im_filename):
    """
    Returns image size, use PIL if present or _no_pil_image_size if no PIL is found.
    """
    assert os.path.isfile(im_filename) # Make sure the file exists
    size = _getCachedFile(im_filename)

    if size is None:
        try:
            if HAS_PIL:
                size = Image.open(im_filename).size
            else:
                size = _noPilImageSize(im_filename)
        except Exception, err:
            # this goes to webserver error log
            import sys
            print >>sys.stderr, '[GET IMAGE SIZE] error %s for file %r' % (err, im_filename)
            return None, None
        #
        if size is not None:
            _setCachedFile(im_filename, size)
        else:
            return None, None
    #
    return size