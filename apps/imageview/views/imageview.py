from django.core.extensions import render_to_response, DjangoContext
from django.models.imageview import images
from django.models.auth import users
from django.utils.httpwrappers import HttpResponseRedirect
from django.conf.settings import MEDIUM_WIDTH, MEDIUM_HEIGHT, THUMBNAIL_SIZE
from django.conf.settings import BG_HIGHLIGHT_CLIP, BG_METHOD
from django.conf.settings import APP_ROOT_URLS
from fiftyfive.apps.imageview.helpers import coloravg, colorconvert
from fiftyfive.apps.imgtool.helpers.utils import make_proxy, make_thumbnail, get_image_size
from fiftyfive.context_processors.processors import get_app_url

# internal helper functions
def _getLatestUploadDateForPhotographer(photographer):
    return images.get_latest(photographer__id__exact=photographer.id).upload_date

def _getLatestIndexForPhotographer(photographer):
    return images.get_object(photographer__id__exact=photographer.id,
                             order_by=['-picture_index'], limit=1).picture_index

# views
def showMedium(request, object_slug):
    cd = {}

    try:
        im = images.get_object(slug__exact=object_slug)
    except images.ImageDoesNotExist:
        return index(request)

    cd['image'] = im
    cd['bgcolor'] = colorconvert.RGBToHTMLColor(
        BG_METHOD(fn=im.get_full_filename(), level=BG_HIGHLIGHT_CLIP) )
    cd['is_earliest'] = (im == images.get_earliest_by_index())
    cd['is_latest'] = (im == images.get_latest_by_index())
    cd['img_url'] = make_proxy(im.get_full_url(), width=MEDIUM_WIDTH, height=MEDIUM_HEIGHT)
    width, height = get_image_size(cd['img_url'])
    cd['img_width'] = width
    cd['img_height'] = height
    cd['r_margin'] = int( (660-width) / 2.)
    cd['ie_r_margin'] = cd['r_margin'] - 3
    

    if cd['is_earliest']:
        cd['latest_image'] = images.get_latest_by_index()
    if cd['is_latest']:
        cd['earliest_image'] = images.get_earliest_by_index()

    return render_to_response( 'imageview/medium_display', cd,
        context_instance = DjangoContext(request) )

def gallery(request):
    # Get a list of photographer IDs
    ids = [x.values()[0] for x in images.get_values(fields=['photographer'], distinct=True)]
    photographer_list = []
    for i in ids:
        photographer = users.get_object(pk=i)
        photographer.images = photographer.get_imageview_image_list(order_by=['-picture_index'])
        for image in photographer.images:
            image.thumb_url = make_thumbnail(image.get_full_url(), pixels=THUMBNAIL_SIZE)

        photographer_list.append(photographer)

    photographer_list.sort(key=_getLatestIndexForPhotographer, reverse=True)

    cd = {}
    cd['photographer_list'] = photographer_list
    cd['thumb_size'] = THUMBNAIL_SIZE

    return render_to_response( 'imageview/gallery', cd,
        context_instance = DjangoContext(request) )

def index(request):
    im = images.get_latest_by_index()
    return HttpResponseRedirect('%simage/%s/' % (get_app_url(request), im.slug))