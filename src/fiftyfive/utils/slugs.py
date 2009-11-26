import string

def get_all_slugs(model_class, slug_field):
    return model_class.objects.values_list(slug_field, flat=True)


def unique_slug_from_source(slug_source, all_slugs):
    """Ensures a unique slug field by appending an integer counter to duplicate slugs.

    For instance, if you save an object titled Daily Roundup, and the slug daily-roundup
    is already taken, this function will try daily-roundup-2, daily-roundup-3,
    daily-roundup-4, etc, until a unique value is found.
    """

    from django.template.defaultfilters import slugify
    slug = slugify(slug_source)
    if slug in all_slugs:
        import re
        counterFinder = re.compile(r'-\d+$')
        counter = 2
        slug = "%s-%i" % (slug, counter)
        while slug in all_slugs:
            slug = re.sub(counterFinder,"-%i" % counter, slug)
            counter += 1
    return slug


def generate_random_slug(
    size=6, valid_chars=string.ascii_letters + string.digits):
    from random import choice
    return ''.join([choice(valid_chars) for i in xrange(size)])


def generate_random_unique_slug(
    all_slugs, size=6, valid_chars=string.ascii_letters + string.digits):
    slug = generate_random_slug(size, valid_chars)

    while slug in all_slugs:
        slug = generate_random_slug(size, valid_chars)

    return slug
