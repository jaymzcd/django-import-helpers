
def assign_file_to_model(module, model_class=None, file_field='main_image', source_field='body', skip_existing=True, verbose=False):
    """ We tend to have "main image" fields on models that hold a primary image used
    across the sites for things like list pages and headers. Often on import of
    existing data we have images mangled within copy or lists. """

    import urllib2
    from posixpath import basename
    from BeautifulSoup import BeautifulSoup as Soup
    from django.db import IntegrityError
    from django.core.files import File

    if model_class is None:
        model_class = module.capitalize()

    mod = __import__(module)
    model= getattr(getattr(mod, 'models'), model_class)

    items = model.objects.all()

    for item in items:

        if getattr(item, file_field) and skip_existing:
            if verbose:
                print "Skipped %s" % item
            continue

        img_src = Soup(getattr(item, source_field)).find('img')['src']
        file_path = '/tmp/%s' % basename(img_src)
        with open(file_path, 'w') as fd:
            fd.write(urllib2.urlopen(img_src).read())

        try:
            f = File(open(file_path))
            item.main_image = f
            item.save()
        except IntegrityError:
            if verbose:
                print "Error settings for %s" % item
            else:
                pass

        if verbose:
            print "Downloaded to %s and assigned for %s" % (file_path, item)

    if verbose:
        print "Completed all %d %s items" % (items.count(), model.__name__)
