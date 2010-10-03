# Boilerplate for initializing a new Django project

It contains several start-up files and an empty Django project.

Replace all instances of string `PROJECT` with the actual project name.

Fork me and customize it to fit your needs.

## Directory setup

I use the following directory setup pattern for my projects.

* Every site is bound to a directory given by its domain name, e.g. `/usr/local/www/webroot/DOMAIN/`.

* Each environment (staging, production) has a separate folder below it, e.g. `/usr/local/www/webroot/DOMAIN/ENVIRONMENT/`.

* The `create_directory_structure` Fab command creates folders `log`, `site`, `site.git` and `virtualenv` for each environment. Web server and application log files are to be put in `log`. Folder `site.git` is a bare repository to push changes to, and then under `site` it is pulled. The `site` contains everything related to the website (application code, media, configuration files, etc.).

* All the startup-up files and templates this boilerplate provides go directly in `site`. Django based codes (`settings` module, `urls` module, project-specific applications) are placed in folder `PROJECT`. Python packages that cannot be installed via PyPI are to be hosted under `site-packages`. As for git, they can be commited as submodules in the main repository.

* Fab command `bootstrap` initializes the directory setup described so far.
