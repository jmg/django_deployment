from fabric.api import cd, run, sudo, put

from utils.commands import *
from utils.files import upload_template

from config import config


class ServerDeployer(object):
    """
        Server deployer for django applications using fabric.
    """

    def __init__(self, app_dir, app_remote_dir, production):
        """
            Params:
                app_dir: the local app dir.
                app_remote_dir: the remote app dir.
                production: determines if the app is set for production or dev.
        """

        self.app_dir = app_dir
        self.app_remote_dir = app_remote_dir
        self.production = production

    def deploy_django_project(self):
        """
            Copies the local django project to the remote location via scp.
        """

        local_dir = "{0}/*".format(self.app_dir)
        remote_dir = self.app_remote_dir

        mkdir("{0}".format(self.app_remote_dir))
        put(local_dir, remote_dir)

    def install_django_project(self):
        """
            Install the django project, sync the db and run django with gunicorn
        """

        with cd("{0}".format(self.app_remote_dir)):

            pip("install -r requirements.txt")

            with cd("{0}".format(self.app_dir)):

                sed("-i \"s/'ENGINE': '[a-zA-Z0-9._\-]*'/'ENGINE': 'django.db.backends.postgresql_psycopg2'/g\" settings.py")
                sed("-i \"s/'NAME': '[a-zA-Z0-9._\-]*'/'NAME': '{0}'/g\" settings.py".format(self.app_remote_dir))
                sed("-i \"s/'USER': '[a-zA-Z0-9._\-]*'/'USER': '{0}'/g\" settings.py".format(config["postgres_user"]))
                sed("-i \"s/'PASSWORD': '[a-zA-Z0-9._\-]*'/'PASSWORD': '{0}'/g\" settings.py".format(config["postgres_password"]))
                sed("-i \"s/'HOST': '[a-zA-Z0-9._\-]*'/'HOST': 'localhost'/g\" settings.py")

            python("manage.py syncdb --noinput")
            #python("manage.py migrate --noinput")

            self.setup_gunicorn_supervisor()

    def setup_gunicorn_supervisor(self):

        context = {
            "app_remote_name": self.app_remote_dir,
            "app_local_name": self.app_dir,
            "gunicorn_port": config["gunicorn_port"],
            "user": config["user"]
        }
        upload_template("templates/gunicorn_supervisor.conf", "/etc/supervisor/conf.d/{0}_gunicorn.conf".format(self.app_remote_dir), context=context)

        run("supervisorctl reread")
        run("supervisorctl update")

    def setup_virtual_env(self):
        """
            Setup the virtual env and install the django project
        """

        venv("{0}_env".format(self.app_remote_dir), self.install_django_project)

    def setup_db(self):
        """
            Setup the postgres db
        """

        with cd("/var/lib/postgresql"):
            sudo("createdb {0}".format(self.app_remote_dir), user="postgres")

    def add_webserver_virtual_host(self):
        """
            Uploads the virtual host template and restart nginx to update the config
        """

        context = {
            "app": self.app_remote_dir,
            "gunicorn_port": config["gunicorn_port"],
        }

        upload_template("templates/nginx_vhost.conf", "/etc/nginx/sites-available/{0}.conf".format(self.app_remote_dir), context=context)
        run("service nginx restart")

    def clean(self):
        """
            Add some env cleaning tasks here
        """

        pass

    def deploy(self):
        """
            Deployment template method.

            If the production flag is False nginx is not used. Gunicorn runs as the mail server.
            If the production flag is True nginx runs as reverse proxy and gunicorn as backend server.
        """

        self.clean()

        self.setup_db()
        self.deploy_django_project()
        self.setup_virtual_env()

        self.add_webserver_virtual_host()
