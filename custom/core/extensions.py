from django.template import loader
from django.http import HttpResponse

def render_to_response(*args, **kwargs):
    content_type = kwargs.pop('content_type', None)
    status_code = kwargs.pop('status_code', 200)
    response = HttpResponse(loader.render_to_string(*args, **kwargs), mimetype=content_type)
    response.status_code = status_code
    return response
load_and_render = render_to_response # For backwards compatibility.