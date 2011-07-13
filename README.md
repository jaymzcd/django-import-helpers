# Django Import Helpers

## What?

These are scripts that I use from a django shell via iPython. Often when we're
importing data to a site from an existing source/model/sql/spreadsheet there's
some tidy up required to get the data fully clean. These are general scripts
I use to aid that process.

In all cases the module & model_class arguments are used to dynamically import
the django model class and get|set-attr are used so you can use these functions
with anything you would normally import and operate on via the shell.

## Functions

### assign_file_to_model

    assign_file_to_model(module, model_class=None, file_field='main_image', source_field='body', skip_existing=True, verbose=False):

Uses the source field to find the first image tag, download that to tmp and then
assign it via django's Files so you end up with the correct paths and the media
in your upload_to path for the object instance.


### slug_model

    slug_model(module, model_class=None, slug_field='slug', source_field='name', skip_existing=True, verbose=False)`

Uses a given field to create a slug which is then assigned to the slug_field. If
the db complains of IntegrityErrors when saving it will append a hash of the current
time and append that and try again to force uniqueness.

