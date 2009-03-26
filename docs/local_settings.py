# Tuple of fully qualified Django settings modules
# These are imported at the end of the main settings file

local_settings = (
    'fiftyfive.settings.includes.dev_george',   # Settings for the main project
    'fiftyfive.apps.imageview.settings.main',   # Settings for ImageView
    'fiftyfive.apps.imgtool.settings.main',     # Settings for ImgTool
)