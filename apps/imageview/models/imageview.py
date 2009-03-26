from django.core import meta
from django.models.auth.users import User

picture_index_help_text = """\
Put in an index number to place this picture in a specific spot on the stream.
Otherwise the system will automatically make it the latest one.
"""

class Image(meta.Model):
    full = meta.ImageField(
        'full size image',
        upload_to = 'imageview/data/full/%Y_%m_%d',
        height_field = 'full_height',
        width_field = 'full_width'
        )

    full_height = meta.IntegerField(editable=False, null=True)

    full_width = meta.IntegerField(editable=False, null=True)

    upload_date = meta.DateTimeField(
        'uploaded date & time',
        default = meta.LazyDate(),
        blank = True,
        editable = False
        )

    title = meta.CharField(maxlength=200)

    photographer = meta.ForeignKey(User)

    description = meta.TextField(blank=True, null=True)

    slug = meta.SlugField(maxlength=200, editable=False, null=True, unique=True)

    picture_index = meta.IntegerField(blank=True, null=True, help_text=picture_index_help_text)

    # Module level methods
    def _module_get_earliest():
        try:
            return get_object(order_by=['upload_date'], limit=1)
        except:
            raise ImageDoesNotExist

    def _module_get_latest_by_index():
        try:
            return get_object(order_by=['-picture_index'], limit=1)
        except:
            raise ImageDoesNotExist

    def _module_get_earliest_by_index():
        try:
            return get_object(order_by=['picture_index'], limit=1)
        except:
            raise ImageDoesNotExist

    # Custom object methods
    def get_medium_factor(self):
        from django.conf.settings import MEDIUM_WIDTH, MEDIUM_HEIGHT
        return min(float(MEDIUM_WIDTH)/self.full_width, float(MEDIUM_HEIGHT)/self.full_height)

    def get_medium_width(self):
        return int(self.full_width * self.get_medium_factor())

    def get_medium_height(self):
        return int(self.full_height * self.get_medium_factor())

    def get_next_by_index(self):
        try:
            return get_object(picture_index__gt=self.picture_index,
                              order_by=['picture_index'], limit=1)
        except:
            raise ImageDoesNotExist

    def get_previous_by_index(self):
        try:
            return get_object(picture_index__lt=self.picture_index,
                              order_by=['-picture_index'], limit=1)
        except:
            raise ImageDoesNotExist

    # Internal helper methods
    def _dummy(self):
        pass

    def _make_slug(self):
        from django.core.template.defaultfilters import slugify
        self.slug = slugify("%s_%s" % (self.title, self.id))

    def _rearrange_index(self, save=False):
        from django.models.imageview import images
        # If some smartypants is entering illegal numbers,
        # but make sure we're not catching NEW images
        if self.picture_index == 0:
            self.picture_index = 1
        # if the image doesn't already have a picutre_index, set it to the latest
        # only for save=True
        if save and (not self.picture_index):
            try:
                self.picture_index = images.get_latest_by_index().picture_index + 1
            except (ImageDoesNotExist, TypeError):
                self.picture_index = self.id

        # Now rearrange the picture_index
        iml = images.get_list(order_by=['picture_index'])
        # If this is not a new record
        if self.id:
            for im in iml[:]:
                # self.id at this point is a string for some reason
                if int(im.id) == int(self.id):
                    iml.remove(im)
                    break

        # if save=True, we have to insert the picture in the right place
        if save:        
            iml.insert(self.picture_index - 1, self)

        # And now we save to the db, overriding the _pre_save() so we don't
        # run into recursion problems.
        for i in range(len(iml)):
            iml[i].picture_index = i+1
            iml[i]._pre_save = self._dummy
            iml[i].save()


    # modifier class methods
    def _pre_save(self):
        # Due to the double save() bug #639 with FileField, we must check to make
        # sure that the file has been uploaded
        if self.full:
            self._make_slug()
            self._rearrange_index(save=True)

    def _post_delete(self):
        from fiftyfive.apps.imgtool.helpers.utils import remove_model_thumbnails
        remove_model_thumbnails(self)
        self._rearrange_index(save=False)

    def __repr__(self):
        from os.path import split
        return "%s | %s | %s" % (
                self.picture_index,
                self.slug,
                split(self.get_full_filename())[1]
                )

    class META:
        admin = meta.Admin(
            date_hierarchy = 'upload_date',
            list_filter = ('photographer',),
            search_fields = ['title']
            )
        ordering = ["-picture_index"]
        get_latest_by = 'upload_date'
