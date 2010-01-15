from django.db import models

class DirtyFieldsMixin(models.Model):
    """
    The mixin provides a way to track fields that have changed (*dirty* fields)
    since object instantiation or the last save.

    ``self._original_state`` represents the original data as a dictionary in the
    form of ``{'field1': field_value, 'related_field2': related_object}``.

    ``self._dirty_fields`` represents the difference between the model object's
    current state vs. ``self._original_state``. The difference is represented as
    a dictionary in the form of ``{'field1': {'old': old_value, 'new': new_value}}``.

    Usage::

      from django.db.models import Model
      from fiftyfive.models.mixins import DirtyFieldsMixin

      class SomeModel(DirtyFieldsMixin, Model):
          # Django field definitions
          def save(self, force_insert=False, force_update=False):
              # You can do interesting stuff here with self._original_state
              # and self._dirty_fields
              super(SomeModel, self).save(force_insert=force_insert,
                                          force_update=force_update)
              # You can do more interesting stuff with self._original_state
              # and self._dirty_fields, as they haven't changed yet.
              # If you want to update self._original_state to reflect the changes,
              # you will have to explicitly call self.update_original_state()
              # either here in the model.save() override, or on the model object
              # externally.
              self.update_original_state()
    """

    def __init__(self, *args, **kwargs):
        super(DirtyFieldsMixin, self).__init__(*args, **kwargs)
        self._original_state_ = self._as_dict()

    def _as_dict(self):
        fields = dict()
        for f in self._meta.fields:
            try:
                fields[f.name] = getattr(self, f.name)
            except f.rel.to.DoesNotExist:
                fields[f.name] = None
        return fields

    def _get_dirty_fields(self):
        new_state = self._as_dict()
        dirty = dict()
        for k, v in self._original_state.iteritems():
            if v != new_state[k]:
                dirty[k] = {'old': v, 'new': new_state[k]}
        return dirty
    _dirty_fields = property(_get_dirty_fields)

    def _get_original(self):
        return self._original_state_
    _original_state = property(_get_original)

    def update_original_state(self):
        self._original_state_ = self._as_dict()

    class Meta:
        abstract=True
