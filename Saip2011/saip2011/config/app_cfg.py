# -*- coding: utf-8 -*-
"""
Global configuration file for TG2-specific settings in Saip2011.

This file complements development/deployment.ini.

Please note that **all the argument values are strings**. If you want to
convert them into boolean, for example, you should use the
:func:`paste.deploy.converters.asbool` function, as in::
    
    from paste.deploy.converters import asbool
    setting = asbool(global_conf.get('the_setting'))
 
"""

from tg.configuration import AppConfig

import saip2011
from saip2011 import model
from saip2011.lib import app_globals, helpers 

base_config = AppConfig()
base_config.renderers = []

base_config.package = saip2011

#Set the default renderer
base_config.default_renderer = 'genshi'
base_config.renderers.append('genshi')
# if you want raw speed and have installed chameleon.genshi
# you should try to use this renderer instead.
# warning: for the moment chameleon does not handle i18n translations
#base_config.renderers.append('chameleon_genshi')

#Configure the base SQLALchemy Setup
base_config.use_sqlalchemy = True
base_config.model = saip2011.model
base_config.DBSession = saip2011.model.DBSession

#Mis configuraciones
base_config.sa_auth.translations.users = 'usuarios' #Group.users
base_config.sa_auth.translations.user_name = 'alias' #User.user_name
base_config.sa_auth.translations.group_name = 'nombrerol' #Group.group_name
base_config.sa_auth.translations.groups = 'roles' #User.group y Permission.groups
base_config.sa_auth.translations.permission_name = 'nombreprivilegio' #Permission.permission_name
base_config.sa_auth.translations.permissions = 'privilegios' #User.permissions y Group.permissions
#base_config.sa_auth.translations.validate_password = 'privilegios' #User.validate_password

# YOU MUST CHANGE THIS VALUE IN PRODUCTION TO SECURE YOUR APP
base_config.sa_auth.cookie_secret = "ChangeME"

# Configure the authentication backend
base_config.auth_backend = 'sqlalchemy'
base_config.sa_auth.dbsession = model.DBSession
# what is the class you want to use to search for users in the database
base_config.sa_auth.user_class = model.Usuario
# what is the class you want to use to search for groups in the database
base_config.sa_auth.group_class = model.Rol
# what is the class you want to use to search for permissions in the database
base_config.sa_auth.permission_class = model.Privilegios


# override this if you would like to provide a different who plugin for
# managing login and logout of your application
base_config.sa_auth.form_plugin = None

# You may optionally define a page where you want users to be redirected to
# on login:
base_config.sa_auth.post_login_url = '/post_login'

# You may optionally define a page where you want users to be redirected to
# on logout:
base_config.sa_auth.post_logout_url = '/post_logout'
