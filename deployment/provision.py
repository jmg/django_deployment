from utils.commands import *
from deploy import ServerDeployer


class ServerProvisioner(ServerDeployer):

    def install_apt_get_dependencies(self):
        """
            Installs OS dependencies (ubuntu/debian) for the python packages.
            Installs the webserver and the db server.
        """

        apt_get("update")
        apt_get("upgrade -y")
        apt_get("install libpq-dev python-dev -y")
        apt_get("install postgresql postgresql-contrib -y")
        apt_get("build-dep python-psycopg2 -y")
        apt_get("install nginx -y")
        apt_get("install supervisor -y")
        apt_get("install memcached -y")
        apt_get("install libmemcached-dev -y")
        apt_get("install libxml2-dev libxslt1-dev -y")
        apt_get("install python-pip -y")

    def install_pip_dependencies(self):
        """
            Install virtualenv as a global package.
            The rest of the packages (dependencies for each app should go on a venv).
        """

        pip("install virtualenv")
        pip("install virtualenvwrapper")

    def deploy(self):
        """
            Provision the server and deploy.
        """

        self.install_apt_get_dependencies()
        self.install_pip_dependencies()

        ServerDeployer.deploy(self)
