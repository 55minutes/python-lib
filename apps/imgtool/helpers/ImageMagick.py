import os
from django.conf import settings

def executeIM(im_util, im_params, in_path, out_path):
    im_cmd = r' '.join(['"%s"' % os.path.join(settings.IMAGEMAGICK_ROOT, im_util),
                        in_path, im_params, out_path])

    return os.system(im_cmd)

def im_width_height(width, height):
    # Figure out width or height constraints to pass to IM
    if width and height:
        pass
    elif width:
        height = ''
    else:
        width = ''

    return width, height

def convert(in_path, out_path, im_params):
    """\
    Generic method to invoke ImageMagick convert command line utility.
    in_path: input image file path
    out_path: output image file path
    im_params: a string of command line params as described in http://www.imagemagick.org/script/command-line-options.php
    """

    IM_UTIL = 'convert'

    # Check if the destination directory exists
    if not os.path.isdir(os.path.dirname(out_path)):
        os.makedirs(os.path.dirname(out_path))

    return executeIM(IM_UTIL, im_params, in_path, out_path)

def resize(in_path, out_path, width=0, height=0, density=False):
    # one of width/height is required
    assert (width > 0) or (height > 0)
    width, height = im_width_height(*map(int, (width, height)))
    if density:
        im_params = '-resize %sx%s -unsharp 0 -strip -density %s' %(width, height, density)
    else:
        im_params = '-resize %sx%s -unsharp 0' %(width, height)
    return convert(in_path, out_path, im_params)

def resize_and_crop(in_path, out_path,
                    resize_w=0, resize_h=0,
                    crop_w=0, crop_h=0,
                    x_offset=0, y_offset=0,
                    density=False):
    # one of width/height is required
    assert (resize_w > 0) or (resize_h > 0)
    resize_w, resize_h = im_width_height(*map(int, (resize_w, resize_h)))
    assert (crop_w > 0) and (crop_h > 0)
    resize_w,resize_h,crop_w,crop_h,x_offset,y_offset = map(int, (
        resize_w, resize_h, crop_w, crop_h, x_offset, y_offset))
    if density:
        im_params = '-resize %sx%s -crop %sx%s+%s+%s -unsharp 0 -strip -density %s' %(
            resize_w, resize_h, crop_w, crop_h, x_offset, y_offset, density)
    else:
        im_params = '-resize %sx%s -crop %sx%s+%s+%s -unsharp 0' %(
            resize_w, resize_h, crop_w, crop_h, x_offset, y_offset)
    return convert(in_path, out_path, im_params)
