import sys
from fabfile import deploy

from fabric.tasks import execute


def run(args):
    """
        Runs the fabric deploy command.

        Params:
            args[0]: The app local directory
            args[1]: The app remote directory
    """

    if not args:
        exit("App not specified")

    app_dir = args[0]

    if len(args) > 1:
        remote_dir = args[1]
    else:
        remote_dir = app_dir

    execute(deploy, app_dir=app_dir, app_remote_dir=remote_dir)


if __name__ == "__main__":

    run(sys.argv[1:])
