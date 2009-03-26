# Settings for George's development environment

DEBUG = True
TEMPLATE_DEBUG = True

ADMINS = (
    ('George Song', 'george@55minutes.com'),
)

MANAGERS = ADMINS

# Make this unique, and don't share it with anybody.
SECRET_KEY = '7$9sc&r&m4ji_q=+(pg4_n^%k$ocp5&4yn%ku@dxp473*w1b)z'

# DB Settings
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = ur'C:/Workspace/django/db/55minutes'

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'America/Los_Angeles PST8PDT SystemV/PST8PDT US/Pacific US/Pacific-New'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ur'C:/Workspace/django/projects/fiftyfive/media/'

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

PRJ_ROOT_URL = 'http://localhost:8000'

APP_ROOT_URLS = {
    'thebook': 'thebook'
    }
