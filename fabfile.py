"""Fabric file for deploying the washingtonsalaries service to an
Ubuntu host.

Example usage:

  fab deploy[:deployment_tar=build/deployment.tar.gz] \
      -i /path/to/public/key \
      -H <user>@<host>
"""
import os
import textwrap

from fabric.api import *
from fabric.contrib import files


__all__ = ['deploy']

env.root = os.path.dirname(env.real_fabfile)
env.jetty_home = '/opt/jetty'
env.jetty_port = 80
env.jetty_user = 'jetty'


def install_dependencies():
    sudo('apt-get update')
    dependencies = [
        'openjdk-7-jre',
        ]
    for dep in dependencies:
        sudo('apt-get install {0} --assume-yes'.format(dep))


def create_config_file():
    files.append(
        filename='/etc/default/jetty',
        text=textwrap.dedent("""\
          JAVA_OPTIONS="-Dsolr.solr.home={jetty_home}/solr ${{JAVA_OPTIONS}}"
          NO_START=0
          JETTY_HOME={jetty_home}
          JETTY_RUN={jetty_home}
          JETTY_ARGS=jetty.port={jetty_port}
          """.format(**env)))


def enable_setuid():
    """Configures Jetty's SetUID feature. This allows Jetty to run on port
    80 as a non-root user.
    """
    with cd(env.jetty_home):
        sudo('ln -s libsetuid-linux.so lib/setuid/libsetuid.so')
        files.append(
            filename='start.ini',
            text=textwrap.dedent("""\
                # ===========================================================
                # setuid settings
                # -----------------------------------------------------------
                --exec
                -Djava.library.path={jetty_home}/lib/setuid

                OPTIONS=setuid
                jetty.startServerAsPrivileged=true
                jetty.username={jetty_user}
                jetty.groupname={jetty_user}
                jetty.umask=002
                etc/jetty-setuid.xml
                """.format(**env)))


def deploy(deployment_tar=None):
    if not deployment_tar:
        local(os.path.join(env.root, 'scripts', 'build'))
        deployment_tar = os.path.join(env.root, 'build', 'deployment.tar.gz')

    install_dependencies()

    put(deployment_tar, '/tmp')
    with cd('/tmp'):
        sudo('tar xzvf {0}'.format(os.path.basename(deployment_tar)))
        sudo('mv jetty {jetty_home}'.format(**env))

    sudo('useradd {jetty_user} -U'.format(**env))
    sudo('chown -R {jetty_user}:{jetty_user} {jetty_home}'.format(**env))

    sudo('ln -s {jetty_home}/bin/jetty.sh /etc/init.d/jetty'.format(**env))

    create_config_file()
    enable_setuid()

    sudo('service jetty start')  # Starts Jetty.
    sudo('update-rc.d jetty defaults')  # Ensures that Jetty is
                                        # started on reboot.
