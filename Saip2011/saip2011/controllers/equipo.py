# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, request, redirect
from datetime import datetime
from tg.controllers import RestController, redirect
from tg.decorators import expose, validate
from formencode.validators import DateConverter, Int, NotEmpty

from pylons.i18n import ugettext as _, lazy_ugettext as l_
from repoze.what import predicates
import transaction
from saip2011.lib.base import BaseController
from saip2011.model import DBSession, metadata

from saip2011.controllers.error import ErrorController
from saip2011 import model
from saip2011.model.auth import Usuario , Rol , Privilegios
from saip2011.model.fase import Fase
from saip2011.model.tipo_fase import Tipo_Fase
from saip2011.model.item import Item
from saip2011.model.equipo_desarrollo import Equipo_Desarrollo
from saip2011.model.tipo_item import Tipo_Item
from saip2011.model.proyecto import Proyecto
from saip2011.model.historial import Historial
from saip2011.model.tipo_campos import Tipo_Campos
 
from cherrypy import HTTPRedirect
from genshi.template import TemplateLoader
import os
from saip2011.form import UsuarioForm , RolForm , PrivilegioForm , FaseForm , TipoFaseForm 
from saip2011.form import ItemForm , TipoItemForm , EquipoForm , ProyectoForm , TipoCamposForm
from formencode import Invalid
from psycopg2 import IntegrityError



class EquipoController(BaseController):
    

 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


	@expose('saip2011.templates.miembro.equipo')
	def equipo(self):
		"""
		   Menu para Equipo de Desarrollo
		"""
		return dict(pagina="equipo")
    
	@expose('saip2011.templates.miembro.listar_miembro')
	def listar_miembro(self):
		"""Lista equipos 
		"""
		equipos =  Equipo_Desarrollo.get_miembros_by_proyecto(self.get_proyecto_actual())
		return dict(pagina="listar_miembro",equipos=equipos)

	@expose('saip2011.templates.miembro.agregar_miembro')
	def agregar_miembro(self, *args, **kw):
		roles = DBSession.query(Rol).all()
		usuarios = DBSession.query(Usuario).all()	

		return dict(pagina="agregar_miembro",values=kw, roles=roles, usuarios=usuarios)
    
	@validate({'idusuario':Int(not_empty=True),
				'idrol':Int(not_empty=True)}, error_handler=agregar_miembro)

	@expose()
	def post_miembro(self, idusuario, idrol):
		if idusuario is not None:
			idusuario = int(idusuario)      
		if idrol is not None:
			idrol = int(idrol)      

		equipo =  Equipo_Desarrollo(proyecto=self.get_proyecto_actual(), idusuario=idusuario, 
									idrol=idrol)
      
		usuario = DBSession.query(Usuario).get(idusuario)
		rol = DBSession.query(Rol).get(idrol)
		usuario.roles=rol

		DBSession.add(equipo)
		DBSession.flush()

		flash("Miembro Agregado Agregado!")  
		redirect('./equipo')

	@expose('saip2011.templates.miembro.editar_miembro')
	def editar_miembro(self, id_equipo, *args, **kw):
      
		usuarios = DBSession.query(Usuario).all()
		roles = DBSession.query(Rol).all()
		equipo = DBSession.query(Equipo_Desarrollo).get(id_equipo)
		
		values = dict(id_equipo=equipo.id_equipo, 
				  nombre_usuario=equipo.nombre_usuario, 
				  nombre_rol=equipo.nombre_rol
		                  )
		                  
		values.update(kw)

		return dict(values=values, usuarios=usuarios, roles=roles)

	@validate({'idusuario':Int(not_empty=True),
		'idrol':Int(not_empty=True)}, error_handler=editar_miembro)

	@expose()
	def put_miembro(self, id_equipo, idusuario, idrol, **kw):
		equipo = DBSession.query(Equipo_Desarrollo).get(id_equipo)
        
		if idusuario is not None:
			idusuario = int(idusuario)      
		if idrol is not None:
		   idrol = int(idrol)   
            
		equipo.idusuario = idusuario
		equipo.idrol=idrol
        
		DBSession.flush()
		flash("Miembro Modificado!")  
		redirect('/equipo')
 
	@expose('saip2011.templates.miembro.eliminar_miembro')
	def eliminar_miembro(self,id_equipo, *args, **kw):
		equipo = DBSession.query(Equipo_Desarrollo).get(id_equipo)	

		values = dict(id_equipo=equipo.id_equipo, 
		      nombre_usuario=equipo.nombre_usuario, 
		      nombre_rol=equipo.nombre_rol
                      )

		return dict(pagina="eliminar_miembro",values=values)

	@validate({'nombre_usuario':NotEmpty,
		'nombre_rol':NotEmpty}, error_handler=eliminar_miembro)

	@expose()
	def post_delete_miembro(self, id_equipo, nombre_usuario, nombre_rol, **kw):
		DBSession.delete(DBSession.query(Equipo_Desarrollo).get(id_equipo))
		DBSession.flush()	
		flash("Miembro eliminado!")
		redirect('/equipo')

