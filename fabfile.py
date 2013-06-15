"""Defines the steps necessary to set up the Washington State
Employees' Salary Database service.

Example usage:

  fab full_deploy:debug=True -i /path/to/public/key -H <user>@<host>

NOTE TO SELF: DO NOT USE THIS FOR AN ACTUAL DEPLOYMENT. LOTS OF
HARDENING MUST TAKE PLACE FIRST.
"""

from fabric.api import *
import os
import sys
import tempfile

__all__ = ['prep_deployment', 'deploy_to_host', 'full_deploy']

env.root = os.path.dirname(env.real_fabfile)


def prep_jetty_files():
    local('unzip {root}/lib/jetty* -d {temp_dir}'.format(**env))
    local('mv {temp_dir}/jetty* {temp_dir}/jetty'.format(**env))

    # Disables the Jetty demos.
    local('rm {jetty_home}/start.d/900-demo.ini'.format(**env))

    # Copies the static files to Jetty's webapps/.
    local('rm -rf {jetty_home}/webapps/ROOT'.format(**env))
    local('cp -r {root}/client {jetty_home}/webapps/ROOT'.format(**env))

    # Copies the Solr home dir to the Jetty dir.
    local('cp -r {root}/solr {jetty_home}'.format(**env))

    # Copies the Solr dependencies into Jetty.
    local('cp {root}/lib/solr*/solr*.war {jetty_home}/webapps/solr.war'.format(
            **env))
    local('cp {root}/lib/solr*/solrj-lib/* {jetty_home}/lib/ext'.format(**env))


def populate_solr():
    local("""
        {root}/data/add_to_solr {root}/data/data.csv {local_server_port} \
                                                     {lines_to_process}
        """.format(lines_to_process=100 if env.debug else '', **env))


def start_jetty(run_fn):
    run_fn("""
        JAVA_OPTIONS="-Dsolr.solr.home={jetty_home}/solr/home $JAVA_OPTIONS" \
        JETTY_RUN=/tmp \
        {jetty_home}/bin/jetty.sh -d start
        """.format(**env))


def stop_jetty(run_fn):
    run_fn('JETTY_RUN=/tmp {jetty_home}/bin/jetty.sh -d stop'.format(**env))


def copy_files_to_host():
    put('{temp_dir}/deployment.tar.gz'.format(**env), '/tmp')

    with cd('/tmp'):
        run('tar xzvf deployment.tar.gz')

        jetty_home_dir = os.path.dirname(env.jetty_home)
        run('mv jetty {0}'.format(jetty_home_dir))


def install_dependencies():
    dependencies = [
        'openjdk-7-jre',
        ]
    for dep in dependencies:
        sudo('apt-get install {0} --assume-yes'.format(dep))


def prep_deployment(debug=None):
    env.temp_dir = tempfile.mkdtemp()
    env.jetty_home = os.path.join(env.temp_dir, 'jetty')
    env.debug = debug if debug is not None else env.debug
    env.local_server_port = 8080

    prep_jetty_files()
    stop_jetty(local)
    start_jetty(local)
    populate_solr()
    stop_jetty(local)
    with lcd(env.temp_dir):
        local('tar zcvf deployment.tar.gz jetty')
    print 'Deployment files available at:', env.temp_dir


def deploy_to_host(temp_dir=None):
    env.temp_dir = temp_dir or env.temp_dir
    if not env.temp_dir:
        abort('Could not resolve the directory containing the files to deploy.')

    env.jetty_home = '/opt/jetty/'
    copy_files_to_host()
    install_dependencies()
    stop_jetty(run)
    start_jetty(run)


def full_deploy(debug=False):
    prep_deployment(debug)
    deploy_to_host()

    if not env.debug:
        local('rm -rf {temp_dir}'.format(**env))
    else:
        print 'Deployment files available at:', env.temp_dir
