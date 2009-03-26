IMAGEMAGICK_ROOT = ur'/usr/local/bin' # Where is the executable for ImageMagick
PROXY_RELATIVE_PATH = 'proxies' # Relative path of proxies to the original image
PROXY_GLOB = '%s_p_w%s_h%s_d%s' # The proxy filename pattern based on the original filename

# Load installation specific settings
try:
    from local_configs import *
    from local_settings import local_settings
    local_settings = locals()[local_settings]
    for s in local_settings:
        exec "from %s import *" % s
except:
    import sys
    sys.stderr.write("Error: Problems processing your local settings.")
    raise