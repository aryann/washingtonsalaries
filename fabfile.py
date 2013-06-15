"""Defines the steps necessary to set up the Washington State
Employees' Salary Database service.
"""

from fabric.api import *
import os
import sys
import tempfile

__all__ = ['prep_deployment']

env.root = os.path.dirname(env.real_fabfile)


def prep_jetty():
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
        {root}/data/add_to_solr {root}/data/data.csv {server_port} \
                                                     {lines_to_process}
        """.format(lines_to_process=100 if env.debug else '', **env))


def start_jetty():
    local("""
        JAVA_OPTIONS="-Dsolr.solr.home={jetty_home}/solr/home $JAVA_OPTIONS" \
        JETTY_RUN=/tmp \
        {jetty_home}/bin/jetty.sh -d start
        """.format(**env))


def stop_jetty():
    local('JETTY_RUN=/tmp {jetty_home}/bin/jetty.sh -d stop'.format(**env))


def prep_deployment(jetty_home=None, debug=False):
    env.temp_dir = tempfile.mkdtemp()
    env.jetty_home = os.path.join(env.temp_dir, 'jetty')
    env.debug = debug
    env.server_port = 8080

    prep_jetty()
    stop_jetty()
    start_jetty()
    populate_solr()
    stop_jetty()

    if not env.debug:
        local('rm -rf {temp_dir}'.format(**env))
    else:
        print 'Deployment files available at:', env.temp_dir
