"""Fabric file for deploying the washingtonsalaries service to an
Ubuntu host.

Example usage:

  fab deploy[:deployment_tar=build/deployment.tar.gz] \
      -i /path/to/public/key \
      -H <user>@<host>
"""
import os
import sys
import tempfile
import textwrap

from fabric.api import *
from fabric.contrib import files


__all__ = ['deploy']

env.root = os.path.dirname(env.real_fabfile)


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
          JETTY_RUN=/var/run
          JETTY_ARGS=jetty.port=80
          """.format(**env)))


def deploy(deployment_tar=None):
    if not deployment_tar:
        local(os.path.join(env.root, 'scripts', 'build'))
        deployment_tar = os.path.join(env.root, 'build', 'deployment.tar.gz')

    env.deployment_tar = deployment_tar
    env.jetty_home = '/opt/jetty'

    install_dependencies()

    put(env.deployment_tar, '/tmp')
    with cd('/tmp'):
        run('tar xzvf {0}'.format(os.path.basename(env.deployment_tar)))
        run('mv jetty {jetty_home}'.format(**env))

    run('ln -s {jetty_home}/bin/jetty.sh /etc/init.d/jetty'.format(**env))
    create_config_file()
    run('service jetty start')  # Starts Jetty.
    run('update-rc.d jetty defaults')  # Ensures that Jetty is started
                                       # on reboot.
