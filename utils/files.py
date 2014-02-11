import shutil
from fabric.contrib import files
from fabric.api import run, settings


def upload_template(template_name, remote_name, context=None, overwrite=False):

    if context is None:
        context = {}

    if overwrite:
        with settings(warn_only=True):
            run("rm {0}".format(remote_name))

    files.append(remote_name, render_template(template_name, context))


def render_template(template_name, context):

    with open(template_name) as f:
        return f.read().format(**context)


def make_zip(local_dir, app_name):

    zip_name = "{0}".format(app_name)
    shutil.make_archive(zip_name, format="zip", root_dir=local_dir)
    return "{0}.zip".format(zip_name)
