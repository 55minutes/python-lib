from django.db import models

class ImageField(models.ImageField):
    def save_file(self, new_data, new_object, original_object, change, rel, save):
        models.FileField.save_file(self, new_data, new_object, original_object, change, rel, save)