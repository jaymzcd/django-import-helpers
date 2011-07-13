
def slug_model(module, model_class=None, slug_field='slug', source_field='name', skip_existing=True, verbose=False):
    """ Loops over a given model assigning a slug field to it """

    from django.template.defaultfilters import slugify
    from django.db import IntegrityError
    from datetime import datetime
    from hashlib import md5

    if model_class is None:
        model_class = module.capitalize()

    mod = __import__(module)
    model= getattr(getattr(mod, 'models'), model_class)

    items = model.objects.all()
    for item in items:

        if (getattr(item, slug_field) is not None) and skip_existing:
            if verbose:
                print "Skipped %s" % getattr(item, source_field)
            continue

        slugged = slugify(getattr(item, source_field))

        try:
            setattr(item, slug_field, slugged)
            item.save()
        except IntegrityError:
            hashed = md5('%s%s' % (slugged, datetime.now()))
            setattr(item, slug_field, '%s-%s' % (slugged, hashed))
            item.save()

        if verbose:
            print "Set slug for %s" % (getattr(item, source_field))

    if verbose:
        print "Completed all %d %s items" % (items.count(), model.__name__)
