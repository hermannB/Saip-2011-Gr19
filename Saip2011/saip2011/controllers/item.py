# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, request, redirect
from datetime import datetime
from tg.decorators import expose, validate
from formencode.validators import DateConverter, Int, NotEmpty

from pylons.i18n import ugettext as _, lazy_ugettext as l_
from repoze.what import predicates
import transaction
from saip2011.lib.base import BaseController
from saip2011.model import DBSession, metadata

from saip2011 import model
from saip2011.model.auth import Usuario , Rol , Privilegios
from saip2011.model.fase import Fase
from saip2011.model.tipo_fase import Tipo_Fase
from saip2011.model.item import Item
from saip2011.model.adjunto import Adjunto
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
from saip2011.controllers.error import ErrorController
import base64


class ItemController(BaseController):
    

 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	@expose('saip2011.templates.item.item')
	def item(self):
		"""
		Menu para Item
		"""
		return dict(pagina="item")

	@expose('saip2011.templates.item.listar_item')
	def listar_item_activos (self):
		items = Item.get_item_activados()
		return dict(pagina="listar_item",items=items)

	@expose('saip2011.templates.item.historial')
	def historial (self, id_item):
		items = Item.get_historial(id_item)
		return dict(pagina="historial",items=items)

	@expose('saip2011.templates.item.listar_item eliminados')
	def listar_item_eliminados(self):
		"""Lista de item 
		"""
		items = Item.get_item_eliminados()
		return dict(pagina="listar_item eliminados",items=items)

	@expose('saip2011.templates.item.editar_item')
	def editar_item(self,id_item,*args, **kw):
		item = DBSession.query(Item).get(id_item)
		if request.method != 'PUT':  
			values = dict(id_item=item.id_item, 
						nombre_item=item.nombre_item,        
						codigo_item=item.codigo_item,
						nombre_tipo_item=item.nombre_tipo_item, 
						estado=item.estado,
						adjunto=item.adjunto,
						complejidad=item.complejidad,
						)

		return dict(pagina="editar_item",values=values)

	@validate({'id_item':Int(not_empty=True),
				'nombre_item':NotEmpty,
                'codigo_item':NotEmpty,  
				'adjunto':Int(not_empty=True),
				'complejidad':Int(not_empty=True), 
				'estado':NotEmpty}, error_handler=editar_item)

	@expose()
	def put_item(self, id_item, nombre_item, codigo_item, adjunto, complejidad, estado, **kw):

		item = DBSession.query(Item).get(int(id_item))
		version=item.version+1
		item.estado_oculto="Desactivado"

		item2 = Item (nombre_item=nombre_item , codigo_item=codigo_item , id_tipo_item=item.id_tipo_item , 
					adjunto=adjunto , complejidad=complejidad , estado = estado ,
					fase=RootController.get_fase_actual() , proyecto=RootController.get_proyecto_actual(),
					creado_por =request.identity['repoze.who.userid'], fecha_creacion = item.fecha_creacion ,
					version =version ,estado_oculto="Activo")

		DBSession.add(item2)
		DBSession.flush()
		flash("Item Modificado!")
		redirect('/item/item')

	@expose('saip2011.templates.item.eliminar_item')
	def eliminar_item(self,id_item, *args, **kw):
		item = DBSession.query(Item).get(id_item)	
		values = dict(id_item=item.id_item, 
						nombre_item=item.nombre_item,
						codigo_item=item.codigo_item,
						nombre_tipo_item=item.nombre_tipo_item, 
						estado=item.estado,
						adjunto=item.adjunto,
						complejidad=item.complejidad,
						)

		return dict(pagina="eliminar_item",values=values)

	@validate({'id_item':Int(not_empty=True),
				'nombre_item':NotEmpty, 
				'codigo_item':NotEmpty, 
				'adjunto':Int(not_empty=True),
				'complejidad':Int(not_empty=True), 
				'estado':NotEmpty}, error_handler=eliminar_item
				)

	@expose()
	def post_delete_item(self, id_item, nombre_item, codigo_item, nombre_tipo_item, estado, adjunto, complejidad, **kw):
		item = DBSession.query(Item).get(id_item)
		item.estado_oculto="Eliminado"

		DBSession.flush()
		flash("item eliminado!")
		redirect('/item/item')

	@expose('saip2011.templates.item.revivir_item')
	def revivir_item(self,id_item, *args, **kw):
		item = DBSession.query(Item).get(id_item)	
		values = dict(id_item=item.id_item, 
						nombre_item=item.nombre_item,
						codigo_item=item.codigo_item,
						nombre_tipo_item=item.nombre_tipo_item, 
						estado=item.estado,
						adjunto=item.adjunto,
						complejidad=item.complejidad,
						)

		return dict(pagina="revivir_item",values=values)

	@validate({'id_item':Int(not_empty=True),
				'nombre_item':NotEmpty,
				'codigo_item':NotEmpty,  
				'adjunto':Int(not_empty=True),
				'complejidad':Int(not_empty=True), 
				'estado':NotEmpty}, error_handler=eliminar_item)

	@expose()
	def post_revivir_item(self, id_item, nombre_item , codigo_item,  nombre_tipo_item, estado, adjunto, complejidad, **kw):
		item = DBSession.query(Item).get(id_item)
		item.estado_oculto="Activo"
		DBSession.flush()
		flash("item Revivido!")
		redirect('/item/item')

	@expose('saip2011.templates.item.recuperar_item')
	def recuperar_item(self,id_item, *args, **kw):
		item = DBSession.query(Item).get(id_item)	
		values = dict(id_item=item.id_item, 
						nombre_item=item.nombre_item,
						codigo_item=item.codigo_item,
						nombre_tipo_item=item.nombre_tipo_item, 
						estado=item.estado,
						adjunto=item.adjunto,
						complejidad=item.complejidad,
						)

		return dict(pagina="recuperar_item",values=values)

	@validate({'id_item':Int(not_empty=True),
				'nombre_item':NotEmpty,
				'codigo_item':NotEmpty,  
				'adjunto':Int(not_empty=True),
				'complejidad':Int(not_empty=True), 
				'estado':NotEmpty}, error_handler=eliminar_item
				 )

	@expose()
	def post_recuperar_item(self, id_item, nombre_item, codigo_item,  nombre_tipo_item, estado, adjunto, complejidad, **kw):
		item = Item.version_actual(id_item)
		item.estado_oculto="Desactivado"
		version= item.version+1  
		DBSession.flush()

		item2 = DBSession.query(Item).get(id_item)
		item3 = Item (nombre_item=item2.nombre_item,codigo_item=item2.codigo_item, id_tipo_item=item2.id_tipo_item, adjunto=item2.adjunto,
						complejidad=item2.complejidad, estado = item2.estado ,fase=item2.fase, 
						proyecto=item2.proyecto,creado_por =item2.creado_por, 
						fecha_creacion = item2.fecha_creacion , version =version , estado_oculto="Activo")
	
		DBSession.add(item3)
		DBSession.flush()
		flash("item recuperado!")
		redirect('/item/item')

	@expose('saip2011.templates.item.agregar_item')
	def agregar_item(self, *args, **kw):
		tipos_items = DBSession.query(Tipo_Item).all()	

		return dict(pagina="agregar_item",values=kw, tipos_items=tipos_items)
    
	@validate({'nombre_item':NotEmpty, 
			    'complejidad':Int(not_empty=True), 
			    'estado':NotEmpty}, error_handler=agregar_item
			    )

	@expose()
	def post_item(self, nombre_item, complejidad, estado, adjunto, id_tipo_item):
		if id_tipo_item is not None:
			id_tipo_item = int(id_tipo_item)
		codigo_item=Item.crear_codigo(id_tipo_item)
		item = Item (nombre_item=nombre_item, codigo_item=codigo_item,id_tipo_item=id_tipo_item, 
						complejidad=complejidad, estado = estado ,fase=1, 
						proyecto=1,creado_por ="DANI", 
						fecha_creacion = "12/12/11", version =1 ,estado_oculto="Activo"
						)
		DBSession.add(item)
		DBSession.flush()
		mayor =Item.get_ultimo_id()

		for ad in adjunto:
			encode=base64.b64encode(ad)
			adj = Adjunto (id_item=mayor, archivo=encode)
			DBSession.add(adj)
			DBSession.flush()
		flash("Item Agregado!")  
		redirect('/item/item')



