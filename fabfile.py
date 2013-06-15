"""Defines the steps necessary to set up the Washington State
Employees' Salary Database service.
"""

from fabric.api import *
import os
import sys
import tempfile

env.root = os.path.dirname(env.real_fabfile)

def prep_server():
    env.temp_dir = tempfile.mkdtemp()
    for dep in ['jetty', 'solr']:
        local('unzip {root}/dist/{dep}* -d {temp_dir}'.format(dep=dep, **env))
        local('mv {temp_dir}/{dep}* {temp_dir}/{dep}'.format(dep=dep, **env))
        env[dep + '_dir'] = os.path.join(env.temp_dir, dep)

    # Disables the demos.
    local('rm {jetty_dir}/start.d/900-demo.ini'.format(**env))

    local('rm -rf {jetty_dir}/webapps/ROOT'.format(**env))
    local('cp -r {root}/client {jetty_dir}/webapps/ROOT'.format(**env))

    # Copies the Solr dir to the Jetty dir.
    local('cp -r {root}/solr {jetty_dir}'.format(**env))

    local('mv {solr_dir}/dist/solrj-lib/* {jetty_dir}/lib/ext'.format(
            **env))
    local('mv {solr_dir}/dist/solr*.war {jetty_dir}/webapps/solr.war'.format(
            **env))

    print env

def start(jetty_home):
    local('{jetty_home}/bin/jetty.sh stop'.format(jetty_home=jetty_home))
    local("""
        JAVA_OPTIONS="-Dsolr.solr.home={jetty_home}/solr/home $JAVA_OPTIONS" \
        {jetty_home}/bin/jetty.sh start
        """.format(jetty_home=jetty_home))
