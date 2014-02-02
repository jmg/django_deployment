from fabric.contrib import files


def upload_template(template_name, remote_name, context=None):

    if context is None:
        context = {}

    files.append(remote_name, render_template(template_name, context))


def render_template(template_name, context):

    with open(template_name) as f:
        return f.read().format(**context)
