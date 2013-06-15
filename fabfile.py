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
    local('unzip -q -d {temp_dir} {root}/lib/jetty*'.format(**env))
    local('mv {temp_dir}/jetty* {temp_dir}/jetty'.format(**env))

    # Disables the Jetty demos.
    local('rm {jetty_home}/start.d/900-demo.ini'.format(**env))

    # Copies the static files to Jetty's webapps/.
    local('rm -rf {jetty_home}/webapps/ROOT'.format(**env))
    local('cp -r {root}/client {jetty_home}/webapps/ROOT'.format(**env))

    # Copies the Solr home dir to the Jetty dir.
    local('cp -r {root}/solr {jetty_home}'.format(**env))

    # Copies the Solr dependencies into Jetty.
    local('unzip -q -d {jetty_home}/webapps/solr {root}/lib/solr*/solr*.war'
          .format(**env))
    local('cp {root}/lib/solr*/solrj-lib/* {jetty_home}/lib/ext'.format(**env))


def populate_solr(debug):
    local("""
        {root}/data/add_to_solr {root}/data/data.csv {local_server_port} \
                                                     {lines_to_process}
        """.format(lines_to_process=100 if debug else '', **env))


def start_jetty(run_fn):
    run_fn("""
        JAVA_OPTIONS="-Dsolr.solr.home={jetty_home}/solr/home $JAVA_OPTIONS" \
        JETTY_HOME={jetty_home} \
        JETTY_RUN=/tmp \
        {jetty_home}/bin/jetty.sh -d start
        """.format(**env))


def stop_jetty(run_fn):
    run_fn("""
        JETTY_HOME={jetty_home} \
        JETTY_RUN=/tmp \
        {jetty_home}/bin/jetty.sh -d stop
        """.format(**env))


def copy_files_to_host():
    put('{temp_dir}/deployment.tar.gz'.format(**env), '/tmp')

    with cd('/tmp'):
        run('tar xzf deployment.tar.gz')

        jetty_home_dir = os.path.dirname(env.jetty_home)
        run('mv jetty {0}'.format(jetty_home_dir))


def install_dependencies():
    dependencies = [
        'openjdk-7-jre',
        ]
    for dep in dependencies:
        sudo('apt-get install {0} --assume-yes'.format(dep))


def prep_deployment(debug=False, keep_jetty_running=True):
    env.temp_dir = tempfile.mkdtemp()
    env.jetty_home = os.path.join(env.temp_dir, 'jetty')
    env.local_server_port = 8080

    prep_jetty_files()
    stop_jetty(local)
    start_jetty(local)
    populate_solr(debug)
    if not keep_jetty_running:
        stop_jetty(local)
    with lcd(env.temp_dir):
        local('tar zcf deployment.tar.gz jetty')
    print 'Deployment files available at:', env.temp_dir
    if keep_jetty_running:
        print 'Jetty running at: http://localhost:{0}'.format(
            env.local_server_port)


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
    prep_deployment(debug=debug, keep_jetty_running=False)
    deploy_to_host()

    if not debug:
        local('rm -rf {temp_dir}'.format(**env))
    else:
        print 'Deployment files available at:', env.temp_dir
