# Django settings for 55minutes project.

VERSION = "2.0"

DEBUG = False
TEMPLATE_DEBUG = False

ADMINS = (
    ('George Song', 'george@55minutes.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3' # 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = ur'/hsphere/local/home/fiftyfiv/django/db/55minutes'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'America/New_York EST5EDT SystemV/EST5EDT US/Eastern'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ur'/hsphere/local/home/fiftyfiv/django/projects/fiftyfive/media/'

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'some_gibberish_string'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.core.template.loaders.filesystem.load_template_source',
    'django.core.template.loaders.app_directories.load_template_source',
#     'django.core.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    "django.middleware.common.CommonMiddleware",
    "django.middleware.sessions.SessionMiddleware",
    "django.middleware.doc.XViewMiddleware",
    #"django.middleware.gzip.GZipMiddleware",
    "django.middleware.http.ConditionalGetMiddleware",
)

ROOT_URLCONF = 'fiftyfive.settings.urls.main'

TEMPLATE_DIRS = ()

INSTALLED_APPS = (
        "django.contrib.admin",
        "fiftyfive.apps.imageview",
        "fiftyfive.apps.imgtool",
        "fiftyfive.apps.customtags",
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "fiftyfive.context_processors.processors.install_url"
    )

PRJ_ROOT_URL = 'http://www.55minutes.com'

APP_ROOT_URLS = {
    'thebook': 'thebook'
    }

    
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