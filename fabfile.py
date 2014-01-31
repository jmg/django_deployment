from fabric.api import env

from deployment.deploy import ServerDeployer
from deployment.provision import ServerProvisioner

from config import config


for key, value in config.iteritems():
    setattr(env, key, value)


def deploy(app_dir=None, app_remote_dir=None, production=False):

    ServerDeployer(app_dir=app_dir, app_remote_dir=app_remote_dir, production=production).deploy()


def full_deploy(app_dir=None, app_remote_dir=None, production=False):

    ServerProvisioner(app_dir=app_dir, app_remote_dir=app_remote_dir, production=production).deploy()
