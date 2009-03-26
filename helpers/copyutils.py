from django.db.models.fields.related import OneToOneField
from django.utils.datastructures import SortedDict

def duplicate_model_recursive(obj):
    "Recursively create copies a model and its related models"
    new_obj = duplicate_model(obj)
    
    # Fetch a recursive collection of the related models for this object.
    # Only objects which appear in this collection will be duplicated
    obj_list = SortedDict()
    obj._collect_sub_objects(obj_list)
    
    _do_copy_recursive(new_obj, obj.id, obj_list)
    
    return new_obj

def _do_copy_recursive(obj, orig_id, obj_list, calldepth=0):
    # Iterate over all the ForeignKey and OneToOneField relationships
    # for this model
    rl = type(obj)._meta.get_all_related_objects()
    for rel in rl:
        rel_cls = rel.model
        rel_field = rel.field.attname
        
        for sub_obj in obj_list.get(rel_cls, {}).values():
            if not getattr(sub_obj, rel_field) == orig_id:
                continue
            
            new_sub_obj = rel_cls(**sub_obj.__dict__)
            new_sub_obj.id = None
            setattr(new_sub_obj, rel_field, obj.id)
            new_sub_obj.save()
            
            # We don't recurse into models that don't have an ID
            # (E.g, OneToOneField)
            if getattr(sub_obj, 'id', False):
                _do_copy_recursive(new_sub_obj, sub_obj.id, obj_list, calldepth + 1)

def duplicate_model(obj):
    "Create a copy of a model"
    cls = type(obj)
    new_obj = cls(**obj.__dict__)
    new_obj.id = None
    new_obj.save()
    return new_obj
