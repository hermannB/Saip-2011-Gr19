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
from saip2011.model.variables import Variables
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



class Tipo_FaseController(BaseController):
    

 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


	@expose('saip2011.templates.tipo_fase.tipo_fase')
	def tipo_fase(self):
		"""
		   Menu para Tipos de Fase
		"""
		return dict(pagina="tipo_fase")

	@expose('saip2011.templates.tipo_fase.editar_tipo_fase')
	def editar_tipo_fase(self,id_tipo_fase,*args, **kw):
		tipo_fase = DBSession.query(Tipo_Fase).get(id_tipo_fase)
		if request.method != 'PUT':  

			values = dict(id_tipo_fase=tipo_fase.id_tipo_fase, 
							nombre_tipo_fase=tipo_fase.nombre_tipo_fase, 
							descripcion=tipo_fase.descripcion,
							)

		return dict(pagina="editar_tipo_fase",values=values)


	@validate({'id_tipo_fase':Int(not_empty=True), 
				'nombre_tipo_fase':NotEmpty, 
				#   'descripcion':NotEmpty
				}, error_handler=editar_tipo_fase)	

	@expose()
	def put_tipo_fase(self, id_tipo_fase, nombre_tipo_fase, descripcion, **kw):
		tipo_fase = DBSession.query(Tipo_Fase).get(id_tipo_fase)

		tipo_fase.nombre_tipo_fase = nombre_tipo_fase
		tipo_fase.descripcion = descripcion

		DBSession.flush()
		flash("Tipo de Fase modificada!")
		redirect('/tipo_fase')

    
	@expose('saip2011.templates.tipo_fase.listar_tipo_fase')
	def listar_tipo_fase(self):
		"""Lista tipos de fases 
		"""
		tipos_fases = Tipo_Fase.get_tipo_fase()
		return dict(pagina="listar_tipo_fase",tipos_fases=tipos_fases)

	@expose('saip2011.templates.tipo_fase.eliminar_tipo_fase')
	def eliminar_tipo_fase(self,id_tipo_fase, *args, **kw):
		tipo_fase = DBSession.query(Tipo_Fase).get(id_tipo_fase)	
		values = dict(id_tipo_fase=tipo_fase.id_tipo_fase, 
						nombre_tipo_fase=tipo_fase.nombre_tipo_fase, 
						descripcion=tipo_fase.descripcion,
						)

		return dict(pagina="eliminar_tipo_fase",values=values)

	@validate({'id_tipo_fase':Int(not_empty=True), 
				'nombre_tipo_fase':NotEmpty, 
				#      'descripcion':NotEmpty
				}, error_handler=eliminar_tipo_fase)	

	@expose()
	def post_delete_tipo_fase(self, id_tipo_fase, nombre_tipo_fase, descripcion, **kw):
	
		DBSession.delete(DBSession.query(Tipo_Fase).get(id_tipo_fase))
		DBSession.flush()
		flash("Tipo de Fase eliminada!")
		redirect('/tipo_fase')

	@expose('saip2011.templates.tipo_fase.agregar_tipo_fase')
	def agregar_tipo_fase(self,cancel=False,**data):
		errors = {}
		tipo_fase = None
		if request.method == 'POST':
			if cancel:
				redirect('/tipo_fase')
			form = TipoFaseForm()
			try:
				data = form.to_python(data)
				tipo_fase = Tipo_Fase(nombre_tipo_fase=data.get('nombre_tipo_fase'),descripcion=data.get('descripcion'))
				DBSession.add(tipo_fase)
				DBSession.flush()
				print tipo_fase
				flash("Tipo de Fase agregada!")

			except Invalid, e:
				print e
				tipo_fase = None
				errors = e.unpack_errors()
				flash(_("Favor complete los datos requeridos"),'warning')

			except IntegrityError:
				flash("LLave duplicada")
				DBSession.rollback()
				redirect('/agregar_tipo_fase')
		else:
			errors = {}        
	        return dict(pagina='agregar_tipo_fase',data=data.get('nombre_tipo_fase'),errors=errors)

 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

