from fabric.api import *
from fabric.contrib.files import *
import os
from copy import copy
import time

"""
    Call this with fab -H <hostname> TASK to deploy THREDDS
    Note: SSH public key must be in /home/thredds/.ssh/authorized_keys
"""

env.user = "thredds"
code_dir = "/home/thredds/maracoos_catalog"
prod_dir = "/var/tomcat/THREDDS_PROD"

def deploy_thredds():
    git_pull()
    copy_catalog()
    copy_styles()
    restart_tomcat()

def git_pull():
    if not exists(code_dir):
        git_clone()
    with cd(code_dir):
        run("git pull origin master")

def git_clone():
    with cd("~"):
        run("rm -rf maracoos_catalog")
        run("git clone https://github.com/asascience-open/maracoos_catalog.git")

def copy_catalog():
    sudo("rsync -av %s/TDS/* %s/content/thredds/" % (code_dir, prod_dir))
    sudo("chown -R tomcat:tomcat %s/content/thredds/*" % prod_dir)

def copy_styles():
    sudo("rsync -av %s/thredds_styles/* %s/webapps/thredds/" % (code_dir, prod_dir))
    sudo("chown -R tomcat:tomcat %s/webapps/thredds/*" % prod_dir)

def restart_tomcat():
    sudo("/etc/init.d/tomcat_thredds restart")
