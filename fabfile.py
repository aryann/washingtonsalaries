"""Defines the steps necessary to set up the Washington State
Employees' Salary Database service.
"""

from fabric.api import *
import os
import sys
import tempfile

env.root = os.path.dirname(env.real_fabfile)


def prep_jetty():
    env.temp_dir = tempfile.mkdtemp()

    local('unzip {root}/lib/jetty* -d {temp_dir}'.format(**env))
    local('mv {temp_dir}/jetty* {temp_dir}/jetty'.format(**env))
    env.jetty_dir = os.path.join(env.temp_dir, 'jetty')

    # Disables the Jetty demos.
    local('rm {jetty_dir}/start.d/900-demo.ini'.format(**env))

    # Copies the static files to Jetty's webapps/.
    local('rm -rf {jetty_dir}/webapps/ROOT'.format(**env))
    local('cp -r {root}/client {jetty_dir}/webapps/ROOT'.format(**env))

    # Copies the Solr home dir to the Jetty dir.
    local('cp -r {root}/solr {jetty_dir}'.format(**env))

    # Copies the Solr dependencies into Jetty.
    local('cp {root}/lib/solr*/solr*.war {jetty_dir}/webapps/solr.war'.format(
            **env))
    local('cp {root}/lib/solr*/solrj-lib/* {jetty_dir}/lib/ext'.format(**env))


def populate_solr(port=8080, debug=False):
    local("""
        {root}/data/add_to_solr {root}/data/data.csv {server_port} \
                                                     {lines_to_process}
        """.format(server_port=port,
                   lines_to_process=100 if debug else '',
                   **env))


def start_jetty(jetty_home=None):
    if jetty_home is None and 'temp_dir' in env:
        jetty_home = os.path.join(env.temp_dir, 'jetty')
    else:
        abort('Could not find Jetty home.')

    local('{jetty_home}/bin/jetty.sh stop'.format(jetty_home=jetty_home))
    local("""
        JAVA_OPTIONS="-Dsolr.solr.home={jetty_home}/solr/home $JAVA_OPTIONS" \
        {jetty_home}/bin/jetty.sh start
        """.format(jetty_home=jetty_home))


def full_deploy(debug=False):
    prep_jetty()
    start_jetty()
    populate_solr(debug=debug)
