from fiftyfive.apps.imageview.helpers import coloravg

# Commenting this out for now. IE is annoying!
#DEFAULT_CONTENT_TYPE = 'application/xhtml+xml'

# function used to get the auto background color
BG_METHOD = coloravg.mostSaturatedDarkSample_highlight_clip

# max medium preview width and height
MEDIUM_WIDTH = 520
MEDIUM_HEIGHT = 480

# thumbnail size
THUMBNAIL_SIZE = 100

# max level for bg color, highlight clipping
BG_HIGHLIGHT_CLIP = 110
