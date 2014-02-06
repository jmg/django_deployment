from fabric.api import env

from deployment.deploy import ServerDeployer
from deployment.provision import ServerProvisioner

from config import config


for key, value in config.iteritems():
    setattr(env, key, value)


def deploy(dir=None, remote_dir=None, name=None, full=False):

    Deployer = ServerProvisioner if full is not False else ServerDeployer
    Deployer(dir=dir, remote_dir=remote_dir, name=name).deploy()
