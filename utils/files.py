import shutil
from fabric.contrib import files


def upload_template(template_name, remote_name, context=None):

    if context is None:
        context = {}

    files.append(remote_name, render_template(template_name, context))


def render_template(template_name, context):

    with open(template_name) as f:
        return f.read().format(**context)


def make_zip(local_dir, app_name):

    zip_name = "{0}".format(app_name)
    shutil.make_archive(zip_name, format="zip", root_dir=local_dir)
    return "{0}.zip".format(zip_name)
