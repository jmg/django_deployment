import sys
import os.path

from fabric.api import cd, run, sudo, put, settings
from fabric.contrib import django
from fabric.contrib.files import exists, append

from utils.commands import *
from utils.files import upload_template

from config import config


class ServerDeployer(object):
    """
        Server deployer for django applications using fabric.
    """

    def __init__(self, dir, remote_dir, name):
        """
            Params:
                dir: the local app dir.
                remote_dir: the remote app dir.
                name: the django project name or package.
        """

        self.app_dir = dir
        self.app_name = os.path.basename(os.path.normpath(self.app_dir))

        self.app_package = name if name else self.app_name
        self.app_remote_dir = remote_dir if remote_dir else self.app_name

        sys.path.append(self.app_dir)
        django.project(self.app_name)

        self.db_name = self.app_name

    def deploy_django_project(self):
        """
            Copies the local django project to the remote location via scp.
        """

        local_dir = "{0}/*".format(self.app_dir)
        app_dir = "{0}".format(self.app_remote_dir)

        if not exists(app_dir):
            mkdir(app_dir)

        put(local_dir, self.app_remote_dir)

    def install_django_project(self):
        """
            Install the django project, sync the db and run django with gunicorn
        """

        from django.conf import settings as django_settings

        with cd("{0}".format(self.app_remote_dir)):

            pip("install -r requirements.txt")

            with cd("{0}".format(self.app_package)):
                self.setup_settings_local()

            self.syncdb(django_settings)
            self.setup_gunicorn_supervisor()

    def setup_settings_local(self):

        line = "\nfrom settings_local import *\n"
        append("settings.py", line)

        context = {
            "db_name": "{0}".format(self.db_name),
            "db_user": "{0}".format(config["postgres_user"]),
            "db_pass": "{0}".format(config["postgres_password"]),
            "db_host": "localhost",
            "db_port": "",
        }

        upload_template("templates/settings_local.conf", "settings_local.py", context)

    def syncdb(self, settings):

        python("manage.py syncdb --noinput")

        if "south" in settings.INSTALLED_APPS:
            python("manage.py migrate --noinput")

    def setup_gunicorn_supervisor(self):

        context = {
            "app_name": self.app_name,
            "app_package": self.app_package,
            "gunicorn_port": config["gunicorn_port"],
            "user": config["user"]
        }
        upload_template("templates/gunicorn_supervisor.conf", "/etc/supervisor/conf.d/{0}_gunicorn.conf".format(self.app_name), context=context)

        run("supervisorctl reread")
        run("supervisorctl update")

    def setup_virtual_env(self):
        """
            Setup the virtual env and install the django project
        """

        venv("{0}_env".format(self.app_name), self.install_django_project)

    def setup_db(self):
        """
            Setup the postgres db
        """

        with cd("/var/lib/postgresql"):
            with settings(warn_only=True):
                sudo("psql -c \"CREATE USER {0} WITH PASSWORD '{1}';\"".format(config["postgres_user"], config["postgres_password"]), user="postgres")
                sudo("createdb {0}".format(self.db_name), user="postgres")
                sudo("psql -c \"GRANT ALL PRIVILEGES ON DATABASE {0} TO {1};\"".format(self.db_name, config["postgres_user"]), user="postgres")

    def add_webserver_virtual_host(self):
        """
            Uploads the virtual host template and restart nginx to update the config
        """

        context = {
            "app": self.app_name,
            "gunicorn_port": config["gunicorn_port"],
        }

        upload_template("templates/nginx_vhost.conf", "/etc/nginx/sites-available/{0}.conf".format(self.app_name), context=context)

        with settings(warn_only=True):
            run("rm /etc/nginx/sites-enabled/default")

        run("ln -s /etc/nginx/sites-available/{app}.conf /etc/nginx/sites-enabled/{app}.conf".format(app=self.app_name))
        run("service nginx restart")

    def clean(self):
        """
            Add some env cleaning tasks here
        """

        pass

    def deploy(self):
        """
            Deployment template method.
        """

        self.clean()

        self.deploy_django_project()
        self.setup_db()
        self.setup_virtual_env()

        self.add_webserver_virtual_host()
