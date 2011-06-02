# -*- coding: utf-8 -*-
"""Setup the Saip2011 application"""

import logging

import transaction
from tg import config

from saip2011.config.environment import load_environment

__all__ = ['setup_app']

log = logging.getLogger(__name__)


def setup_app(command, conf, vars):
    """Place any commands to setup saip2011 here"""
    load_environment(conf.global_conf, conf.local_conf)
    # Load the models
    from saip2011 import model
    print "Creating tables"
    model.metadata.create_all(bind=config['pylons.app_globals'].sa_engine)

    administrador = model.Usuario()
    administrador.alias = u'admin'
    administrador.nombre = u'Administrador'
    administrador.apellido = u'Administrador'
    administrador.email_address = u'admin@somedomain.com'
    administrador.password = u'admin'

    model.DBSession.add(administrador)

    rol = model.Rol()
    rol.nombrerol = u'Administrador'
    rol.descripcion = u'Administrador del Sistema'

    rol.usuarios.append(administrador)

    model.DBSession.add(rol)

    privilegio = model.Privilegios()
    privilegio.nombreprivilegio = u'control_total'
    privilegio.descripcion = u'Este permiso permite el control total del sistema'
    privilegio.roles.append(rol)

    model.DBSession.add(privilegio)

    privilegio2 = model.Privilegios()
    privilegio2.nombreprivilegio = u'solo_lectura'
    privilegio2.descripcion = u'Este permiso permite solo ver las consultas'
    privilegio2.roles.append(rol)

    model.DBSession.add(privilegio2)

    #editor = model.User()
    #editor.user_name = u'editor'
    #editor.display_name = u'Example editor'
    #editor.email_address = u'editor@somedomain.com'
    #editor.password = u'editpass'

    #model.DBSession.add(editor)
    model.DBSession.flush()

    transaction.commit()
    print "Successfully setup"
