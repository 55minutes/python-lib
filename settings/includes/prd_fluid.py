# Settings for George's development environment

DEBUG = False
TEMPLATE_DEBUG = False

ADMINS = (
    ('George Song', 'george@55minutes.com'),
)

MANAGERS = ADMINS

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ab9tG&VKT%RYWtyzJi5PrjOBti0K1c&o**#zs&NbQ$CFrXXv%@'

# DB Settings
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = ur'/hsphere/local/home/fiftyfiv/django/db/55minutes'

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'America/New_York EST5EDT SystemV/EST5EDT US/Eastern'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ur'/hsphere/local/home/fiftyfiv/django/projects/fiftyfive/media/'

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/media/fiftyfive/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

PRJ_ROOT_URL = 'http://www.55minutes.com'

APP_ROOT_URLS = {
    'thebook': 'thebook'
    }