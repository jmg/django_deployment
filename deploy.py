from fabfile import deploy
from fabric.tasks import execute

from optparse import OptionParser


def run():
    """
        Runs the fabric deploy command.
    """

    parser = OptionParser()
    parser.add_option("-d", "--dir", dest="dir", help="The app local directory")
    parser.add_option("-r", "--remote_dir", dest="remote_dir", help="The app remote directory")
    parser.add_option("-n", "--name", dest="name", help="The django app name")
    parser.add_option("-f", "--full", help="Provision before deploy", default=False)
    parser.add_option("-o", "--no_files", help="Don't copy the app files", default=False)

    (options, args) = parser.parse_args()

    execute(deploy, **options.__dict__)


if __name__ == "__main__":

    run()
