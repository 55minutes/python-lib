from django.db import models
from django.contrib.auth.models import User as AuthUser

def _user_display_name(user):
    if user.first_name and user.last_name:
        return u"%s %s" %(user.first_name, user.last_name)

    if user.first_name or user.last_name:
        return u"%s" %(user.first_name or user.last_name)

    if user.email:
        return user.email

    return user.username

def _display_as_last_first(user):
    if user.first_name and user.last_name:
        return u"%s, %s" %(user.last_name, user.first_name)
    else:
        return user.display_name

User = AuthUser
def _get_display_name(self):
    return _user_display_name(self)
User.display_name = property(_get_display_name)
User.display_as_last_first = _display_as_last_first

class AuthUserMixin(models.Model):
    def _get_display_name(self):
        return _user_display_name(self.user)
    display_name = property(_get_display_name)

    def display_as_last_first(self):
        return _display_as_last_first(self.user)

    class Meta:
        abstract=True
