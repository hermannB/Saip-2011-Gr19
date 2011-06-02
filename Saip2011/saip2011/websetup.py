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

#######################################################################################
##		VALORES POR DEFECTO
###################### Privilegios o permisos###########################################


##  usuario


    priv = model.Privilegios()
    priv.nombreprivilegio = u'Agregar Usurio'
    priv.descripcion = u'Brinda las funciones necesarias para ingresar nuevos usuarios al sistema'
    model.DBSession.add(priv)

    priv = model.Privilegios()
    priv.nombreprivilegio = u'Modificar Usurio'
    priv.descripcion = u'Brinda las funciones necesarias para actualizar algun dato perteneciente a algun usuario del sistema'
    model.DBSession.add(priv)

    priv = model.Privilegios()
    priv.nombreprivilegio = u'Eliminar Usurio'
    priv.descripcion = u'Brinda las funciones necesarias para eliminar usuarios que ya no deban tener acceso al sistema'
    model.DBSession.add(priv)

    priv = model.Privilegios()
    priv.nombreprivilegio = u'Cambiar Password'
    priv.descripcion = u'Brinda la funcion con la cual el usuario puede modificar su password'
    model.DBSession.add(priv)


## Rol


    priv = model.Privilegios()
    priv.nombreprivilegio = u'Agregar Rol'
    priv.descripcion = u'Brinda las funciones necesarias para ingresar nuevos roles al sistema'
    model.DBSession.add(priv)

    priv = model.Privilegios()
    priv.nombreprivilegio = u'Modificar Rol'
    priv.descripcion = u'Brinda las funciones necesarias para actualizar algun dato perteneciente a algun rol del sistema'
    model.DBSession.add(priv)

    priv = model.Privilegios()
    priv.nombreprivilegio = u'Eliminar Rol'
    priv.descripcion = u'Brinda las funciones necesarias para eliminar roles que ya no son requeridos'
    model.DBSession.add(priv)


## Tipo de Fase


    priv = model.Privilegios()
    priv.nombreprivilegio = u'Agregar Tipo de Fase'
    priv.descripcion = u'Brinda las funciones necesarias para ingresar nuevos Tipos de Fases al sistema'
    model.DBSession.add(priv)

    priv = model.Privilegios()
    priv.nombreprivilegio = u'Modificar Tipo de Fase'
    priv.descripcion = u'Brinda las funciones necesarias para actualizar algun dato perteneciente a algun Tipo de Fase del sistema'
    model.DBSession.add(priv)

    priv = model.Privilegios()
    priv.nombreprivilegio = u'Eliminar Tipo de Fase'
    priv.descripcion = u'Brinda las funciones necesarias para eliminar algun Tipo de Fase que ya no es requerido'
    model.DBSession.add(priv)


## Fase


    priv = model.Privilegios()
    priv.nombreprivilegio = u'Agregar Fase'
    priv.descripcion = u'Brinda las funciones necesarias para ingresar nuevas Fases al sistema'
    model.DBSession.add(priv)

    priv = model.Privilegios()
    priv.nombreprivilegio = u'Modificar Fase'
    priv.descripcion = u'Brinda las funciones necesarias para actualizar algun dato perteneciente a alguna Fase del sistema'
    model.DBSession.add(priv)

    priv = model.Privilegios()
    priv.nombreprivilegio = u'Eliminar Fase'
    priv.descripcion = u'Brinda las funciones necesarias para eliminar alguna Fase que ya no es requerida'
    model.DBSession.add(priv)

    priv = model.Privilegios()
    priv.nombreprivilegio = u'Crear Linea Base'
    priv.descripcion = u'Brinda la funcion con la cual el Lider de un Proyecto define que una fase esta finalizadad y se puede pasar a la siguiente'
    model.DBSession.add(priv)


## Item


    priv = model.Privilegios()
    priv.nombreprivilegio = u'Agregar Item'
    priv.descripcion = u'Brinda las funciones necesarias para ingresar nuevos Items al sistema'
    model.DBSession.add(priv)

    priv = model.Privilegios()
    priv.nombreprivilegio = u'Modificar Item'
    priv.descripcion = u'Brinda las funciones necesarias para actualizar algun dato perteneciente a algun Item del sistema'
    model.DBSession.add(priv)

    priv = model.Privilegios()
    priv.nombreprivilegio = u'Eliminar Item'
    priv.descripcion = u'Brinda las funciones necesarias para eliminar algun Item que ya no es requerido (eliminacion logica)'
    model.DBSession.add(priv)

    priv = model.Privilegios()
    priv.nombreprivilegio = u'Aprobar Item'
    priv.descripcion = u'Brinda la funcion con la cual el Lider de un Proyecto marca un Item para indicar que cumple con su finalidad'
    model.DBSession.add(priv)


## Tipo de Item


    priv = model.Privilegios()
    priv.nombreprivilegio = u'Agregar Tipo de Item'
    priv.descripcion = u'Brinda las funciones necesarias para ingresar nuevos Tipos de Items al sistema'
    model.DBSession.add(priv)

    priv = model.Privilegios()
    priv.nombreprivilegio = u'Modificar Tipo de Item'
    priv.descripcion = u'Brinda las funciones necesarias para actualizar algun dato perteneciente a algun Tipo de Item del sistema'
    model.DBSession.add(priv)

    priv = model.Privilegios()
    priv.nombreprivilegio = u'Eliminar Tipo de Item'
    priv.descripcion = u'Brinda las funciones necesarias para eliminar algun Tipo de Item que ya no es requerido (eliminacio logica)'
    model.DBSession.add(priv)


##  Proyecto


    priv = model.Privilegios()
    priv.nombreprivilegio = u'Agregar Proyecto'
    priv.descripcion = u'Brinda las funciones necesarias para ingresar nuevos Proyecto al sistema'
    model.DBSession.add(priv)

    priv = model.Privilegios()
    priv.nombreprivilegio = u'Modificar Proyecto'
    priv.descripcion = u'Brinda las funciones necesarias para actualizar algun dato perteneciente a algun Proyecto del sistema'
    model.DBSession.add(priv)

    priv = model.Privilegios()
    priv.nombreprivilegio = u'Eliminar Proyecto'
    priv.descripcion = u'Brinda las funciones necesarias para eliminar algun Proyecto que ya no es requerido (cambio de estado)'
    model.DBSession.add(priv)


##   Equipo de desarrollo


    priv = model.Privilegios()
    priv.nombreprivilegio = u'Agregar Miembros de un Equipo'
    priv.descripcion = u'Brinda las funciones necesarias para ingresar nuevos Miembros de un Equipo de Desarrollo al sistema'
    model.DBSession.add(priv)

    priv = model.Privilegios()
    priv.nombreprivilegio = u'Modificar Miembro de un Equipo'
    priv.descripcion = u'Brinda las funciones necesarias para actualizar a algun Miembro de un Equipo de Desarrollo del sistema'
    model.DBSession.add(priv)

    priv = model.Privilegios()
    priv.nombreprivilegio = u'Eliminar Miembros de un Equipo'
    priv.descripcion = u'Brinda las funciones necesarias para eliminar algun Miembro de un Equipo de Desarrollo que ya no es requerido'
    model.DBSession.add(priv)
   


##  Reportes   ---------faltan mas


    priv = model.Privilegios()
    priv.nombreprivilegio = u'Indice de Impacto'
    priv.descripcion = u'Calcula el Impacto que tendra la modificacion o eliminacion de un determinado Item con relacion al proyecto'
    model.DBSession.add(priv)


###################### Tipos de Fases ##################################################
   

    tipo = model.Tipo_Fase()
    tipo.nombre_tipo_fase = u'Analisis de Requerimiento'
    tipo.descripcion = u'ERS'
    model.DBSession.add(tipo)

    tipo = model.Tipo_Fase()
    tipo.nombre_tipo_fase = u'Disenho y Arquitectura'
    tipo.descripcion = u'DCU'
    model.DBSession.add(tipo)

    tipo = model.Tipo_Fase()
    tipo.nombre_tipo_fase = u'Programacion'
    tipo.descripcion = u'Codigo'
    model.DBSession.add(tipo)

    tipo = model.Tipo_Fase()
    tipo.nombre_tipo_fase = u'Pruebas'
    tipo.descripcion = u'test'
    model.DBSession.add(tipo)

    tipo = model.Tipo_Fase()
    tipo.nombre_tipo_fase = u'Mantenimiento'
    tipo.descripcion = u'todo'
    model.DBSession.add(tipo)

    model.DBSession.flush()
    transaction.commit()
    print "Successfully setup"
