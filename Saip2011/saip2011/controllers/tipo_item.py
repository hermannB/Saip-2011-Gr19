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
from saip2011.form import UsuarioForm , RolForm , PrivilegioForm , FaseForm
from saip2011.form import ItemForm , TipoItemForm , EquipoForm , ProyectoForm 
from saip2011.form import TipoFaseForm , TipoCamposForm

from formencode import Invalid
from psycopg2 import IntegrityError



class Tipo_ItemController(BaseController):
    

################################################################################

    @expose('saip2011.templates.tipo_item.listar_tipo_item')
    def tipo_item(self):
        """
           Menu para Tipos de Item
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")
        tipos_items = Tipo_Item.get_tipo_item()
        tipos_campos = Tipo_Campos.get_tipo_campos()
        return dict(pagina="listar_tipo_item",tipos_items=tipos_items, 
                    tipos_campos=tipos_campos,nom_proyecto=nom_proyecto
                    ,nom_fase=nom_fase)
        #return dict(pagina="tipo_item",nom_proyecto=nom_proyecto)

################################################################################
       
    @expose('saip2011.templates.tipo_item.listar_tipo_item')
    def listar_tipo_item(self):
        """Lista tipos de items 
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")
        tipos_items = Tipo_Item.get_tipo_item()
        tipos_campos = Tipo_Campos.get_tipo_campos()
        return dict(pagina="listar_tipo_item",tipos_items=tipos_items, 
                    tipos_campos=tipos_campos,nom_proyecto=nom_proyecto
                    ,nom_fase=nom_fase)

###############################################################################

    @expose('saip2011.templates.tipo_item.listar_mis_campos')
    def ver_campos(self,id_tipo_item):
        """Lista  
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")
        tipo_item=Tipo_Item.get_tipo_item_by_id(int(id_tipo_item))
        values = dict(id_tipo_item=tipo_item.id_tipo_item, 
				        nombre_tipo_item=tipo_item.nombre_tipo_item, 
				        descripcion=tipo_item.descripcion
				        )

        camp =Tipo_Campos.get_campos_by_tipo_item(tipo_item.id_tipo_item)
        campos = []
        for c in camp:
            campos.append(c)
        return dict(pagina="listar_mis_campos",campos=campos,
                        nom_proyecto=nom_proyecto,nom_fase=nom_fase,
                        values=values)

 ################################################################################


    @expose('saip2011.templates.tipo_item.editar_tipo_item')
    def editar_tipo_item(self,id_tipo_item,*args, **kw):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")
        tipo_item = DBSession.query(Tipo_Item).get(id_tipo_item)
        campos2=Tipo_Campos.get_campos_by_tipo_item(tipo_item.id_tipo_item)
        valores_permitidos=["alfanumerico","numerico","fecha"]
        if request.method != 'PUT':  
            values = dict(id_tipo_item=tipo_item.id_tipo_item, 
							nombre_tipo_item=tipo_item.nombre_tipo_item, 
                            codigo_tipo_item=tipo_item.codigo_tipo_item,
							descripcion=tipo_item.descripcion,
							)

        return dict(pagina="editar_tipo_item",values=values,campos2=campos2,
                        nom_proyecto=nom_proyecto,nom_fase=nom_fase,
                        valores_permitidos=valores_permitidos)

    @validate({'id_tipo_item':Int(not_empty=True),
				'nombre_tipo_item':NotEmpty, 
				#               'descripcion':NotEmpty
				}, error_handler=editar_tipo_item)	

    @expose()
    def put(self, id_tipo_item, nombre_tipo_item, codigo_tipo_item,
                    descripcion, campo,valor,**kw):
        tipo_item = DBSession.query(Tipo_Item).get(id_tipo_item)
        campos2=Tipo_Campos.get_campos_by_tipo_item(tipo_item.id_tipo_item)

        for cam in campos2:
            DBSession.delete(DBSession.query(Tipo_Campos).get
                                (cam.id_tipo_campos))
            DBSession.flush()

        tipo_item.nombre_tipo_item = nombre_tipo_item
        tipo_item.descripcion = descripcion
        tipo_item.codigo_tipo_item=codigo_tipo_item

        if campo is not None:
            if not isinstance(campo, list):
                campo = [campo]

        if valor is not None:
            if not isinstance(valor, list):
                valor = [valor]

        indice=0
             
        for c in campo:
            camp =Tipo_Campos(id_tipo_item=id_tipo_item,
                                nombre_campo=c,
                                valor_campo=valor[indice])
            indice+=1
            DBSession.add(camp)
        DBSession.flush()
        flash("Tipo de Item modificada!")
        redirect('/tipo_item/tipo_item')

################################################################################


    @expose('saip2011.templates.tipo_item.clonar_tipo_item')
    def clonar_tipo_item(self,id_tipo_item,*args, **kw):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")
        tipo_item = DBSession.query(Tipo_Item).get(id_tipo_item)
        valores_permitidos=["alfanumerico","numerico","fecha"]
        campos = Tipo_Campos.get_campos_by_tipo_item(tipo_item.id_tipo_item)

        if request.method != 'PUT':  
            values = dict( id_tipo_item=tipo_item.id_tipo_item, 
							nombre_tipo_item=tipo_item.nombre_tipo_item, 
                            codigo_tipo_item=tipo_item.codigo_tipo_item,
							descripcion=tipo_item.descripcion
							)

        return dict(pagina="clonar_tipo_item",values=values,campos=campos,
                        nom_proyecto=nom_proyecto,nom_fase=nom_fase,
                        valores_permitidos=valores_permitidos)

    @validate({'nombre_tipo_item':NotEmpty, 
				#'descripcion':NotEmpty
				}, error_handler=clonar_tipo_item)	

    @expose()
    def put_item(self, nombre_tipo_item,codigo_tipo_item,
                     descripcion, campo,valor,**kw):
        tipo_item = Tipo_Item (nombre_tipo_item=nombre_tipo_item,
                                    descripcion=descripcion,
                                    codigo_tipo_item=codigo_tipo_item)
        DBSession.add(tipo_item)

        if campo is not None:
            if not isinstance(campo, list):
                campo = [campo]

        if valor is not None:
            if not isinstance(valor, list):
                valor = [valor]

        indice=0
        id_tipo=Tipo_Item.get_ultimo_id()        
        for c in campo:
            camp =Tipo_Campos(id_tipo_item=id_tipo,
                                nombre_campo=c,
                                valor_campo=valor[indice])
            indice+=1
            DBSession.add(camp)
        DBSession.flush()
        flash("Tipo de Item clonada!")
        redirect('/tipo_item/tipo_item')

################################################################################

    @expose('saip2011.templates.tipo_item.eliminar_tipo_item')
    def eliminar_tipo_item(self,id_tipo_item, *args, **kw):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")
        tipo_item = DBSession.query(Tipo_Item).get(id_tipo_item)	
        values = dict(id_tipo_item=tipo_item.id_tipo_item, 
						nombre_tipo_item=tipo_item.nombre_tipo_item, 
                        codigo_tipo_item=tipo_item.codigo_tipo_item,
						descripcion=tipo_item.descripcion,
						)
        return dict(pagina="eliminar_tipo_item",values=values,
                        nom_proyecto=nom_proyecto,nom_fase=nom_fase)

    @validate({'id_tipo_item':Int(not_empty=True), 
				'nombre_tipo_item':NotEmpty, 
                'codigo_tipo_item':NotEmpty, 
				#               'descripcion':NotEmpty
				}, error_handler=eliminar_tipo_item)	

    @expose()
    def post_delete(self, id_tipo_item, nombre_tipo_item, codigo_tipo_item,
                        descripcion, **kw):
        campos2=Tipo_Campos.get_campos_by_tipo_item(id_tipo_item)

        for cam in campos2:
            DBSession.delete(DBSession.query(Tipo_Campos).get
                                (cam.id_tipo_campos))
            DBSession.flush()

        DBSession.delete(DBSession.query(Tipo_Item).get(id_tipo_item))
        DBSession.flush()
        flash("Tipo de Item eliminado!")
        redirect('/tipo_item/tipo_item')

################################################################################

    @expose('saip2011.templates.tipo_item.agregar_tipo_item')
    def agregar_tipo_item(self, *args, **kw):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")
        return dict(pagina="agregar_tipo_item",values=kw,
                        nom_proyecto=nom_proyecto,nom_fase=nom_fase)
    
    @validate({'nombre_tipo_item':NotEmpty, 
                'codigo_tipo_item':NotEmpty, 
				#'descripcion':NotEmpty
				}, error_handler=agregar_tipo_item)

    @expose()
    def post_tipo_item(self, nombre_tipo_item, codigo_tipo_item, descripcion,
                        campo, valor):
        tipo_item = Tipo_Item (nombre_tipo_item=nombre_tipo_item,
                                codigo_tipo_item=codigo_tipo_item,
                                descripcion=descripcion)
        DBSession.add(tipo_item)

        if campo is not None:
            if not isinstance(campo, list):
                campo = [campo]

        if valor is not None:
            if not isinstance(valor, list):
                valor = [valor]

        indice=0
        id_tipo=Tipo_Item.get_ultimo_id()        
        for c in campo:
            camp =Tipo_Campos(id_tipo_item=id_tipo,
                                nombre_campo=c,
                                valor_campo=valor[indice])
            indice+=1
            DBSession.add(camp)

        flash("Tipo Item Agregado!")  
        redirect('/tipo_item/tipo_item')

