from pysqlite2 import dbapi2 as sqlite
import re

"""
1. Create the following holding table:

BEGIN;
CREATE TABLE "imageview_images1" (
    "id" integer NOT NULL PRIMARY KEY,
    "full" varchar(100) NOT NULL,
    "full_height" integer NOT NULL,
    "full_width" integer NOT NULL,
    "upload_date" datetime NOT NULL,
    "title" varchar(200) NOT NULL,
    "photographer_id" integer NOT NULL REFERENCES "auth_users" ("id"),
    "description" text NOT NULL,
    "slug" varchar(200) NULL,
    "picture_index" integer NULL
);
COMMIT;

2. "django-admin sqlclear imageview" and run the script

3. "django-admin install imageview"

4. INSERT INTO imageview_images SELECT * FROM imageview_images1;

5. DROP TABLE imageview_images1;
"""

def slugify(value):
    "Converts to lowercase, removes non-alpha chars and converts spaces to hyphens"
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return re.sub('\s+', '-', value)

def old_row_generator(db):
    sql = """\
    SELECT  *
    FROM    imageview_images
    """
    c = db.cursor()
    c.execute(sql)
    for row in c:
        yield row

def new_row_generator(db):
    for row in old_row_generator(db):
        row = list(row)
        slug = slugify("%s_%s" % (row[5], row[0]))
        row.insert(-1, slug)
        yield tuple(row)


def insert_date(db):
    sql = """\
    INSERT  INTO    imageview_images1
    VALUES  (?,?,?,?,?,?,?,?,?,?)
    """
    c = db.cursor()
    c.executemany(sql, new_row_generator(db))

if __name__ == '__main__':
    insert_date(sqlite.connect('/home/George/workspace/django/db/55minutes',
                               isolation_level=None))