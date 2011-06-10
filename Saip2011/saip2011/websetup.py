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
	privilegio.nombreprivilegio = u'Control Total'
	privilegio.var = u'control_total'
	privilegio.descripcion = u'Este permiso otorga todas las funcionalidades del sistema'
	privilegio.roles.append(rol)
	model.DBSession.add(privilegio)


	rolUB = model.Rol()
	rolUB.nombrerol = u'Usuario Basico'
	rolUB.descripcion = u'Usuario Basico'
	model.DBSession.add(rolUB)

	rolLP = model.Rol()
	rolLP.nombrerol = u'Lider Proyecto'
	rolLP.descripcion = u'Lider del Proyecto'

	model.DBSession.add(rolLP)


	model.DBSession.flush()



#######################################################################################

###################### Privilegios o permisos###########################################


##  usuario

	priv = model.Privilegios()
	priv.nombreprivilegio = u'Lider del proyecto '
	priv.var = u'lider'
	priv.descripcion = u'Brinda las funciones necesarias para el lider del proyecto'
	priv.roles.append(rolLP)
	model.DBSession.add(priv)
    
	priv = model.Privilegios()
	priv.nombreprivilegio = u'Usuario basico '
	priv.var = u'usuario_basico'
	priv.descripcion = u'Brinda las funciones necesarias para un usuario basico'
	priv.roles.append(rolUB)
	model.DBSession.add(priv)

	priv = model.Privilegios()
	priv.nombreprivilegio = u'Agregar Usuario al '
	priv.var = u'alta_usuario'
	priv.descripcion = u'Brinda las funciones necesarias para ingresar nuevos usuarios al sistema'
	model.DBSession.add(priv)

	priv = model.Privilegios()
	priv.nombreprivilegio = u'Listar Usuario'
	priv.var = u'list_usuario'
	priv.descripcion = u'Brinda las funciones necesarias para realizar un listado de los ususario del Sistema'
	model.DBSession.add(priv)

	priv = model.Privilegios()
	priv.nombreprivilegio = u'Modificar Usuario'
	priv.var = u'mod_usuario'
	priv.descripcion = u'Brinda las funciones necesarias para actualizar algun dato perteneciente a algun usuario del sistema'
	model.DBSession.add(priv)

	priv = model.Privilegios()
	priv.nombreprivilegio = u'Eliminar Usuario'
	priv.var = u'elim_usuario'
	priv.descripcion = u'Brinda las funciones necesarias para eliminar usuarios que ya no deban tener acceso al sistema'
	model.DBSession.add(priv)

	priv = model.Privilegios()
	priv.nombreprivilegio = u'Cambiar Password'
	priv.var = u'cam_pass'
	priv.descripcion = u'Brinda la funcion con la cual el usuario puede modificar su password'
	priv.roles.append(rolUB)
	priv.roles.append(rolLP)
	model.DBSession.add(priv)


## Rol


	priv = model.Privilegios()
	priv.nombreprivilegio = u'Agregar Rol'
	priv.var = u'alta_rol'
	priv.descripcion = u'Brinda las funciones necesarias para ingresar nuevos roles al sistema'
	priv.roles.append(rolLP)
	model.DBSession.add(priv)

	priv = model.Privilegios()
	priv.nombreprivilegio = u'Listar Rol'
	priv.var = u'list_rol'
	priv.descripcion = u'Brinda las funciones necesarias para realizar un listado de los roles del Sistema'
	priv.roles.append(rolLP)
	model.DBSession.add(priv)

	priv = model.Privilegios()
	priv.nombreprivilegio = u'Modificar Rol'
	priv.var = u'mod_rol'
	priv.descripcion = u'Brinda las funciones necesarias para actualizar algun dato perteneciente a algun rol del sistema'
	priv.roles.append(rolLP)
	model.DBSession.add(priv)

	priv = model.Privilegios()
	priv.nombreprivilegio = u'Eliminar Rol'
	priv.var = u'eliminar_rol'
	priv.descripcion = u'Brinda las funciones necesarias para eliminar roles que ya no son requeridos'
	priv.roles.append(rolLP)
	model.DBSession.add(priv)


## Tipo de Fase


	priv = model.Privilegios()
	priv.nombreprivilegio = u'Agregar Tipo de Fase'
	priv.var = u'alta_tipo_fase'
	priv.descripcion = u'Brinda las funciones necesarias para ingresar nuevos Tipos de Fases al sistema'
	priv.roles.append(rolLP)
	model.DBSession.add(priv)

	priv = model.Privilegios()
	priv.nombreprivilegio = u'Listar Tipo de Fase'
	priv.var = u'list_tipo_fase'
	priv.descripcion = u'Brinda las funciones necesarias para realizar un listado de los Tipo de fases dentro del sistema'
	priv.roles.append(rolLP)
	model.DBSession.add(priv)

	priv = model.Privilegios()
	priv.nombreprivilegio = u'Modificar Tipo de Fase'
	priv.var = u'mod_tipo_fase'
	priv.descripcion = u'Brinda las funciones necesarias para actualizar algun dato perteneciente a algun Tipo de Fase del sistema'
	priv.roles.append(rolLP)
	model.DBSession.add(priv)

	priv = model.Privilegios()
	priv.nombreprivilegio = u'Eliminar Tipo de Fase'
	priv.var = u'elim_tipo_fase'
	priv.descripcion = u'Brinda las funciones necesarias para eliminar algun Tipo de Fase que ya no es requerido'
	priv.roles.append(rolLP)
	model.DBSession.add(priv)


## Fase


	priv = model.Privilegios()
	priv.nombreprivilegio = u'Agregar Fase'
	priv.var = u'alta_fase'
	priv.descripcion = u'Brinda las funciones necesarias para ingresar nuevas Fases al sistema'
	priv.roles.append(rolLP)
	model.DBSession.add(priv)

	priv = model.Privilegios()
	priv.nombreprivilegio = u'Listar Fase'
	priv.var = u'list_fase'
	priv.descripcion = u'Brinda las funciones necesarias para realizar un listado de las Fases dentro del sistema'
	priv.roles.append(rolLP)
	model.DBSession.add(priv)

	priv = model.Privilegios()
	priv.nombreprivilegio = u'Modificar Fase'
	priv.var = u'mod_fase'
	priv.descripcion = u'Brinda las funciones necesarias para actualizar algun dato perteneciente a alguna Fase del sistema'
	priv.roles.append(rolLP)
	model.DBSession.add(priv)

	priv = model.Privilegios()
	priv.nombreprivilegio = u'Eliminar Fase'
	priv.var = u'elim_fase'
	priv.descripcion = u'Brinda las funciones necesarias para eliminar alguna Fase que ya no es requerida'
	priv.roles.append(rolLP)
	model.DBSession.add(priv)

	priv = model.Privilegios()
	priv.nombreprivilegio = u'Crear Linea Base'
	priv.var = u'linea_base'
	priv.descripcion = u'Brinda la funcion con la cual el Lider de un Proyecto define que una fase esta finalizadad y se puede pasar a la siguiente'
	priv.roles.append(rolLP)
	model.DBSession.add(priv)


## Item


	priv = model.Privilegios()
	priv.nombreprivilegio = u'Agregar Item'
	priv.var = u'alta_item'
	priv.descripcion = u'Brinda las funciones necesarias para ingresar nuevos Items al sistema'
	priv.roles.append(rolLP)
	model.DBSession.add(priv)

	priv = model.Privilegios()
	priv.nombreprivilegio = u'Listar Item'
	priv.var = u'list_item'
	priv.descripcion = u'Brinda las funciones necesarias para realizar un listado de los Items dentro del sistema'
	priv.roles.append(rolLP)
	model.DBSession.add(priv)

	priv = model.Privilegios()
	priv.nombreprivilegio = u'Modificar Item'
	priv.var = u'mod_item'
	priv.descripcion = u'Brinda las funciones necesarias para actualizar algun dato perteneciente a algun Item del sistema'
	priv.roles.append(rolLP)
	model.DBSession.add(priv)

	priv = model.Privilegios()
	priv.nombreprivilegio = u'Eliminar Item'
	priv.var = u'elim_item'
	priv.descripcion = u'Brinda las funciones necesarias para eliminar algun Item que ya no es requerido (eliminacion logica)'
	priv.roles.append(rolLP)
	model.DBSession.add(priv)

	priv = model.Privilegios()
	priv.nombreprivilegio = u'Revivir Item'
	priv.var = u'rev_item'
	priv.descripcion = u'Brinda las funciones necesarias para eliminar algun Item que ya no es requerido (eliminacion logica)'
	priv.roles.append(rolLP)
	model.DBSession.add(priv)

	priv = model.Privilegios()
	priv.nombreprivilegio = u'Restablecer version de Item'
	priv.var = u'rest_item'
	priv.descripcion = u'Brinda las funciones necesarias para recuperar versiones anteriores de un item que fueron almacenadas en el historial)'
	priv.roles.append(rolLP)
	model.DBSession.add(priv)

	priv = model.Privilegios()
	priv.nombreprivilegio = u'Aprobar Item'
	priv.var = u'aprobar_item'
	priv.descripcion = u'Brinda la funcion con la cual el Lider de un Proyecto marca un Item para indicar que cumple con su finalidad'
	priv.roles.append(rolLP)
	model.DBSession.add(priv)


## Tipo de Item


	priv = model.Privilegios()
	priv.nombreprivilegio = u'Agregar Tipo de Item'
	priv.var = u'alta_tipo_item'
	priv.descripcion = u'Brinda las funciones necesarias para ingresar nuevos Tipos de Items al sistema'
	priv.roles.append(rolLP)
	model.DBSession.add(priv)

	priv = model.Privilegios()
	priv.nombreprivilegio = u'Listar Tipo de Item'
	priv.var = u'list_tipo_item'
	priv.descripcion = u'Brinda las funciones necesarias para realizar un listado de los Tipo de Item dentro del sistema'
	priv.roles.append(rolLP)
	model.DBSession.add(priv)

	priv = model.Privilegios()
	priv.nombreprivilegio = u'Modificar Tipo de Item'
	priv.var = u'mod_tipo_item'
	priv.descripcion = u'Brinda las funciones necesarias para actualizar algun dato perteneciente a algun Tipo de Item del sistema'
	priv.roles.append(rolLP)
	model.DBSession.add(priv)

	priv = model.Privilegios()
	priv.nombreprivilegio = u'Eliminar Tipo de Item'
	priv.var = u'elim_tipo_item'
	priv.descripcion = u'Brinda las funciones necesarias para eliminar algun Tipo de Item que ya no es requerido (eliminacio logica)'
	priv.roles.append(rolLP)
	model.DBSession.add(priv)


##  Proyecto


	priv = model.Privilegios()
	priv.nombreprivilegio = u'Agregar Proyecto'
	priv.var = u'alta_proyecto'
	priv.descripcion = u'Brinda las funciones necesarias para ingresar nuevos Proyecto al sistema'
	model.DBSession.add(priv)

	priv = model.Privilegios()
	priv.nombreprivilegio = u'Listar Proyecto'
	priv.var = u'list_proyecto'
	priv.descripcion = u'Brinda las funciones necesarias para realizar un listado de los Proyectos dentro del sistema'
	model.DBSession.add(priv)

	priv = model.Privilegios()
	priv.nombreprivilegio = u'Modificar Proyecto'
	priv.var = u'mod_proyecto'
	priv.descripcion = u'Brinda las funciones necesarias para actualizar algun dato perteneciente a algun Proyecto del sistema'
	model.DBSession.add(priv)

	priv = model.Privilegios()
	priv.nombreprivilegio = u'Eliminar Proyecto'
	priv.var = u'elim_proyecto'
	priv.descripcion = u'Brinda las funciones necesarias para eliminar algun Proyecto que ya no es requerido (cambio de estado)'
	model.DBSession.add(priv)

	priv = model.Privilegios()
	priv.nombreprivilegio = u'Ingresar Proyecto'
	priv.var = u'ingresar_proyecto'
	priv.descripcion = u'Brinda opcion al usuario de seleccionar uno de los proyectos donde trabaja'
	priv.roles.append(rolLP)
	model.DBSession.add(priv)
	priv.roles.append(rolUB)


##   Equipo de desarrollo


	priv = model.Privilegios()
	priv.nombreprivilegio = u'Agregar Miembros de un Equipo'
	priv.var = u'alta_equipo'
	priv.descripcion = u'Brinda las funciones necesarias para ingresar nuevos Miembros de un Equipo de Desarrollo al sistema'
	priv.roles.append(rolLP)
	model.DBSession.add(priv)

	priv = model.Privilegios()
	priv.nombreprivilegio = u'Listar Miembros de un Equipo'
	priv.var = u'list_miembros'
	priv.descripcion = u'Brinda las funciones necesarias para realizar un listado de los Miembros de un Proyecto del sistema'
	priv.roles.append(rolLP)
	model.DBSession.add(priv)


	priv = model.Privilegios()
	priv.nombreprivilegio = u'Modificar Miembro de un Equipo'
	priv.var = u'mod_equipo'
	priv.descripcion = u'Brinda las funciones necesarias para actualizar a algun Miembro de un Equipo de Desarrollo del sistema'
	priv.roles.append(rolLP)
	model.DBSession.add(priv)

	priv = model.Privilegios()
	priv.nombreprivilegio = u'Eliminar Miembros de un Equipo'
	priv.var = u'elim_equipo'
	priv.descripcion = u'Brinda las funciones necesarias para eliminar algun Miembro de un Equipo de Desarrollo que ya no es requerido'
	priv.roles.append(rolLP)
	model.DBSession.add(priv)



##  Reportes   ---------faltan mas


	priv = model.Privilegios()
	priv.nombreprivilegio = u'Indice de Impacto'
	priv.var = u'impacto'
	priv.descripcion = u'Calcula el Impacto que tendra la modificacion o eliminacion de un determinado Item con relacion al proyecto'
	priv.roles.append(rolLP)
	model.DBSession.add(priv)

	priv = model.Privilegios()
	priv.nombreprivilegio = u'Arbol de Relaciones'
	priv.var = u'relaciones'
	priv.descripcion = u'Realiza un impresion de todos los items relacionados con un determinado Item desde sus antecesores hasta sus sucesores actuales'
	priv.roles.append(rolLP)
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


###################### Variables ##################################################

	var = model.Variables()
	var.nombre = u'usuario_actual'
	var.valor = u''
	model.DBSession.add(var)

	var = model.Variables()
	var.nombre = u'fase_actual'
	var.valor = u'1'
	model.DBSession.add(var)

	var = model.Variables()
	var.nombre = u'proyecto_actual'
	var.valor = u'1'
	model.DBSession.add(var)

	var = model.Variables()
	var.nombre = u'rol_actual'
	var.valor = u'1'
	model.DBSession.add(var)

	var = model.Variables()
	var.nombre = u'rol_por_defecto'
	var.valor = u'2'
	model.DBSession.add(var)

	transaction.commit()
	print "Successfully setup"

