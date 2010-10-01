import os

from fabric.api import *
from fabric.contrib import files, console
from fabric import utils


def _setup_common():
    env.home = '/usr/local/www/webroot/DOMAIN/'
    env.project = 'PROJECT'
    env.site = 'site'
    env.root = os.path.join(env.home, env.environment)
    env.site_dir = os.path.join(env.root, env.site)
    env.virtualenv_root = os.path.join(env.root, 'virtualenv')
    env.settings = '%(project)s.settings' % env


def staging():
    """
    Use staging environment.
    """
    env.user = 'SERVER_USER'
    env.environment = 'staging'
    env.hosts = ['DOMAIN:SERVER_PORT']
    env.shell = '/usr/local/bin/bash -l -c'
    _setup_common()


def production():
    """
    Use production environment.
    """
    utils.abort('Production deployment not yet implemented.')


def bootstrap():
    """
    Initialize environment: create virtualenv, deploy code, install packages.
    """
    require('root', provided_by=('staging', 'production'))
    create_directory_structure()
    create_virtualenv()
    init_repos()
    deploy()
    update_requirements()


def create_directory_structure():
    """
    Create directory structure as follow:

    /environment/
    /environment/log
    /environment/site
    /environment/site.git
    /environment/virtualenv
    """
    require('root', provided_by=('staging', 'production'))
    git_repo = os.path.join(env.root, "%s.git" % env.site)
    run('mkdir -p %(root)s' % env)
    run('mkdir -p %(site_dir)s' % env)
    run('mkdir -p %s' % os.path.join(env.root, 'log'))
    run('mkdir -p %s' % git_repo)


def init_repos():
    """
    Initialize git repositories.

    Create shared repository at site.git/ to accept local pushes. Create
    live repository at site/. Pull changes from shared repository.
    """
    require('root', provided_by=('staging', 'production'))
    git_repo = os.path.join(env.root, "%s.git" % env.site)
    with cd(git_repo):
        run('git --bare init')
    with cd(env.site_dir):
        run('git init')
        run('git remote add origin %s' % git_repo)


def create_virtualenv():
    """
    Setup virtualenv.
    """
    require('virtualenv_root', provided_by=('staging', 'production'))
    args = '--clear --no-site-packages'
    run('virtualenv %s %s' % (args, env.virtualenv_root))


def deploy():
    """
    Push repository.
    """
    require('site_dir', provided_by=('staging', 'production'))
    if env.environment == 'production':
        if not console.confirm('Are you sure you want to deploy production?',
                               default=False):
            utils.abort('Production deployment aborted.')
    local('git push %s %s' % (env.environment, env.environment,))
    with cd(env.site_dir):
        run('git pull origin %s' % env.environment)


def update_requirements():
    """
    Update external package dependencies.
    """
    require('project_dir', provided_by=('staging', 'production'))
    cmd = ['%s install' % os.path.join(env.virtualenv_root, 'bin', 'pip')]
    cmd += ['-E %(virtualenv_root)s' % env]
    cmd += ['-r %s' % os.path.join(env.project_dir, 'requirements.txt')]
    run(' '.join(cmd))


def restart():
    """
    Touch WSGI file to trigger application server reload.
    """
    require('site_dir', provided_by=('staging', 'production'))
    apache_dir = os.path.join(env.site_dir, 'apache')
    with cd(apache_dir):
        run('touch %s-%s.wsgi' % (env.site, env.environment,))


def configtest():
    """
    Test Apache configuration.
    """
    require('root', provided_by=('staging', 'production'))
    run('apachectl configtest')


def apache_reload():
    """
    Reload Apache.
    """
    require('root', provided_by=('staging', 'production'))
    run('sudo /usr/local/etc/rc.d/apache22 reload')


def apache_restart():
    """
    Restart Apache.
    """
    require('root', provided_by=('staging', 'production'))
    run('sudo /usr/local/etc/rc.d/apache22 restart')


def migrate():
    """
    Execute pending data- and schemamigrations.
    """
    require('site_dir', provided_by=('staging', 'production'))
    project_dir = os.path.join(env.site_dir, env.project)
    with cd(project_dir):
        virtualenv('python manage.py migrate')


def virtualenv(cmd):
    """
    Helper function.
    Runs a command using the virtualenv environment
    """
    require('virtualenv_root', provided_by=('staging', 'production'))
    return run('source %s/bin/activate; %s' % (env.virtualenv_root, cmd))

