# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, request, redirect
from datetime import datetime
import time
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
from saip2011.model.variables import Variables
from saip2011.model.adjunto import Adjunto
from saip2011.model.equipo_desarrollo import Equipo_Desarrollo
from saip2011.model.tipo_item import Tipo_Item
from saip2011.model.proyecto import Proyecto
from saip2011.model.historial import Historial
from saip2011.model.tipo_campos import Tipo_Campos
from cherrypy import HTTPRedirect
from genshi.template import TemplateLoader
import os
from saip2011.form import UsuarioForm , RolForm , PrivilegioForm , FaseForm 
from saip2011.form import ItemForm , TipoItemForm , EquipoForm , ProyectoForm 
from saip2011.form import TipoFaseForm , TipoCamposForm
from formencode import Invalid
from psycopg2 import IntegrityError
from saip2011.controllers.error import ErrorController
import base64
import binascii


class ItemController(BaseController):
    

################################################################################
    @expose('saip2011.templates.item.item')
    def item(self):
        """
        Menu para Item
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        fases=Fase.get_fase_by_proyecto(int (Variables.get_valor_by_nombre
                                                ("proyecto_actual")) )
        
        return dict(pagina="listar_fase",fases=fases,nom_proyecto=nom_proyecto)

################################################################################
        
    @expose('saip2011.templates.item.listar_item')
    def listar_item_activos (self):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        id_fase=int(Variables.get_valor_by_nombre("fase_actual"))
        items = Item.get_item_activados_by_fase(id_fase)
        return dict(pagina="listar_item",items=items,nom_proyecto=nom_proyecto)

################################################################################

    @expose('saip2011.templates.item.historial')
    def historial (self, id_item):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        id_fase=int(Variables.get_valor_by_nombre("fase_actual"))
        items = Item.get_historial(id_item)
        return dict(pagina="historial",items=items,nom_proyecto=nom_proyecto)

################################################################################

    @expose('saip2011.templates.item.listar_item eliminados')
    def listar_item_eliminados(self):
        """Lista de item 
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        id_fase=int(Variables.get_valor_by_nombre("fase_actual"))
        items = Item.get_item_eliminados_by_fase(id_fase)
        return dict(pagina="listar_item eliminados",items=items,
                        nom_proyecto=nom_proyecto)

################################################################################

    @expose('saip2011.templates.item.editar_item')
    def editar_item(self,id_item,*args, **kw):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        item = DBSession.query(Item).get(id_item)
        if request.method != 'PUT':  
            values = dict(id_item=item.id_item, 
						nombre_item=item.nombre_item,        
						codigo_item=item.codigo_item,
						nombre_tipo_item=item.nombre_tipo_item, 
						estado=item.estado,
						complejidad=item.complejidad,
						)
        adjuntos=Adjunto.get_adjuntos_by_item(item.id_item)
        #decodificar
        adjuntos2=[]
        for adj in adjuntos:
            var=binascii.b2a_base64(adj.archivo)
            archivo=base64.b64decode(var)
            adjuntos2.append(archivo)

        return dict(pagina="editar_item",values=values,adjuntos2=adjuntos2,
                        nom_proyecto=nom_proyecto)

    @validate({'id_item':Int(not_empty=True),
				'nombre_item':NotEmpty,
                'codigo_item':NotEmpty,  
				'complejidad':Int(not_empty=True), 
				'estado':NotEmpty}, error_handler=editar_item)

    @expose()
    def put_item(self, id_item, nombre_item, nombre_tipo_item, codigo_item,
                     complejidad, estado, **kw):

        item = DBSession.query(Item).get(int(id_item))
        version=item.version+1
        item.estado_oculto="Desactivado"
        DBSession.flush()

        item2 = Item (nombre_item=nombre_item , codigo_item=codigo_item ,
                       id_tipo_item=item.id_tipo_item , complejidad=complejidad,
                       estado = estado ,fase=int( Variables.get_valor_by_nombre
                        ("fase_actual") ) , proyecto=
                        int( Variables.get_valor_by_nombre("proyecto_actual") ),
    					creado_por=Variables.get_valor_by_nombre("usuario_actual")
                        ,fecha_creacion = time.ctime() ,
        				version =version ,estado_oculto="Activo")

        DBSession.add(item2)
        DBSession.flush()
        flash("Item Modificado!")
        redirect('/item/item')

################################################################################

    @expose('saip2011.templates.item.eliminar_item')
    def eliminar_item(self,id_item, *args, **kw):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        item = DBSession.query(Item).get(id_item)	
        values = dict(id_item=item.id_item, 
						nombre_item=item.nombre_item,
						codigo_item=item.codigo_item,
						nombre_tipo_item=item.nombre_tipo_item, 
						estado=item.estado,
						complejidad=item.complejidad,
						)

        return dict(pagina="eliminar_item",values=values,
                        nom_proyecto=nom_proyecto)

    @validate({'id_item':Int(not_empty=True),
				'nombre_item':NotEmpty, 
				'codigo_item':NotEmpty, 
				'complejidad':Int(not_empty=True), 
				'estado':NotEmpty}, error_handler=eliminar_item
				)

    @expose()
    def post_delete_item(self, id_item, nombre_item, codigo_item, nombre_tipo_item,
                         estado, complejidad, **kw):
        item = DBSession.query(Item).get(id_item)
        item.estado_oculto="Eliminado"

        DBSession.flush()
        flash("item eliminado!")
        redirect('/item/item')

################################################################################

    @expose('saip2011.templates.item.revivir_item')
    def revivir_item(self,id_item, *args, **kw):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        item = DBSession.query(Item).get(id_item)	
        values = dict(id_item=item.id_item, 
						nombre_item=item.nombre_item,
						codigo_item=item.codigo_item,
						nombre_tipo_item=item.nombre_tipo_item, 
						estado=item.estado,
						complejidad=item.complejidad,
						)

        return dict(pagina="revivir_item",values=values,
                        nom_proyecto=nom_proyecto)

    @validate({'id_item':Int(not_empty=True),
				'nombre_item':NotEmpty,
				'codigo_item':NotEmpty,  
				'complejidad':Int(not_empty=True), 
				'estado':NotEmpty}, error_handler=eliminar_item)

    @expose()
    def post_revivir_item(self, id_item, nombre_item , codigo_item, 
                            nombre_tipo_item, estado, complejidad, **kw):
        item = DBSession.query(Item).get(id_item)
        item.estado_oculto="Activo"
        DBSession.add(item2)
        DBSession.flush()
        flash("item Revivido!")
        redirect('/item/item')

################################################################################

    @expose('saip2011.templates.item.recuperar_item')
    def recuperar_item(self,id_item, *args, **kw):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        item = DBSession.query(Item).get(id_item)	
        values = dict(id_item=item.id_item, 
						nombre_item=item.nombre_item,
						codigo_item=item.codigo_item,
						nombre_tipo_item=item.nombre_tipo_item, 
						estado=item.estado,
						complejidad=item.complejidad,
						)

        return dict(pagina="recuperar_item",values=values,
                        nom_proyecto=nom_proyecto)

    @validate({'id_item':Int(not_empty=True),
				'nombre_item':NotEmpty,
				'codigo_item':NotEmpty,  
				'complejidad':Int(not_empty=True), 
				'estado':NotEmpty}, error_handler=eliminar_item
				 )

    @expose()
    def post_recuperar_item(self, id_item, nombre_item, codigo_item, 
                nombre_tipo_item, estado, complejidad, **kw):
        item = Item.version_actual(id_item)
        item.estado_oculto="Desactivado"
        version= item.version+1  
        DBSession.flush()

        item2 = DBSession.query(Item).get(id_item)
        item3 = Item (nombre_item=item2.nombre_item,
                        codigo_item=item2.codigo_item, 
                        id_tipo_item=item2.id_tipo_item,
						complejidad=item2.complejidad, estado = item2.estado,
                        fase=item2.fase, proyecto=item2.proyecto,
                        creado_por =item2.creado_por, 
                        fecha_creacion = item2.fecha_creacion ,
                        version =version , estado_oculto="Activo")
	
        DBSession.add(item3)
        DBSession.flush()
        flash("item recuperado!")
        redirect('/item/item')

################################################################################

    @expose('saip2011.templates.item.agregar_item')
    def agregar_item(self, *args, **kw):
        id_fase=int(Variables.get_valor_by_nombre("fase_actual"))
    
        fase = DBSession.query(Fase).get(id_fase)	
        tipos_items=fase.tipos_items
        return dict(pagina="agregar_item",values=kw, tipos_items=tipos_items)
    
    @validate({'nombre_item':NotEmpty, 
			    'complejidad':Int(not_empty=True), 
			    'estado':NotEmpty}, error_handler=agregar_item
			    )

    @expose()
    def post_item(self, nombre_item, adjunto, complejidad, id_tipo_item):
        if id_tipo_item is not None:
            id_tipo_item = int(id_tipo_item)
        tipo_item = DBSession.query(Tipo_Item).get(id_tipo_item)
        pre_codigo=tipo_item.codigo_tipo_item
        proy_act=int (Variables.get_valor_by_nombre("proyecto_actual"))
        fas_act=int (Variables.get_valor_by_nombre("fase_actual"))
        codigo_item=Item.crear_codigo(id_tipo_item,pre_codigo,proy_actual,fas_act)

        item = Item (nombre_item=nombre_item, codigo_item=codigo_item,
                        id_tipo_item=id_tipo_item, 
						complejidad=complejidad, estado = "nuevo", 
                        fase=int(Variables.get_valor_by_nombre("fase_actual")),
						proyecto=int( Variables.get_valor_by_nombre
                                        ("proyecto_actual") ),
						creado_por=Variables.get_valor_by_nombre
                                        ("usuario_actual"),
						fecha_creacion = time.ctime(), version =1 ,
                        estado_oculto="Activo"
						)
        DBSession.add(item)
        DBSession.flush()
        mayor =Item.get_ultimo_id()

        for ad in adjunto:
            encode=base64.b64encode(ad)
            var=binascii.a2b_base64(encode)
            adj = Adjunto (id_item=mayor, archivo=var)
            DBSession.add(adj)
            DBSession.flush()
        flash("Item Agregado!")  
        redirect('/item/item')
################################################################################

