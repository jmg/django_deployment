from fabric.api import run, prefix


def _make_cmd(cmd, **kwargs):
    """
        Delegates the [cmd] parameter to the fabric run command.
    """
    return lambda args: run("{0} {1}".format(cmd, args), **kwargs)


def venv(name, callback):
    """
        Creates and activates a virtualenv using virtualenvwrapper.
        The callback function is called inside the virtualenv context.
    """

    with prefix("export WORKON_HOME=~/Envs"):
        run("mkdir -p $WORKON_HOME")
        with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
            run("mkvirtualenv {0}".format(name))
            with prefix("workon {0}".format(name)):
                callback()


apt_get = _make_cmd("apt-get")
python = _make_cmd("python")
pip = _make_cmd("pip")
sed = _make_cmd("sed")
echo = _make_cmd("echo")
gunicorn = _make_cmd("gunicorn")
mkdir = _make_cmd("mkdir")
