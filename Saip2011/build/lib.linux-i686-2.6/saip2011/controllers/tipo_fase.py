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



class Tipo_FaseController(BaseController):
    
 ################################################################################

    @expose('saip2011.templates.tipo_fase.tipo_fase')
    def tipo_fase(self,start=0,end=5,indice=None,texto=""):
        """
           Menu para Tipos de Fase
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        paginado = 5
        if start <> 0:
            end=int(start.split('=')[1]) #obtiene el fin de pagina
            start=int(start.split('&')[0]) #obtiene el inicio de pagina
        #print start,end
        #total = len(Tipo_Fase.get_tipo_fases())
        pagina_actual = ((start % end) / paginado) + 1
        if ((start % end) % paginado) <> 0:
             pagina_actual = pagina_actual + 1
                
        if indice  <> None and texto <> "":  
            tipos_fases = Tipo_Fase.get_tipo_fase_por_filtro(indice,texto)
            total = len(tipos_fases)
        else:   
            tipos_fases = Tipo_Fase.get_tipo_fase_por_pagina(start,end)
            total = len(Tipo_Fase.get_tipo_fases())

        lista = ['nombre','descripcion']


        return dict(pagina="tipo_fase",tipos_fases=tipos_fases,
                        nom_proyecto=nom_proyecto,nom_fase=nom_fase,
                        inicio=start,fin=end,paginado=paginado,
                        pagina_actual=pagina_actual,total=total,
                        param="/tipo_fase/tipo_fase",lista=lista)


 ################################################################################


    @expose('saip2011.templates.tipo_fase.editar_tipo_fase')
    def editar_tipo_fase(self,id_tipo_fase,*args, **kw):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        if id_tipo_fase is not None:
            id_tipo_fase=int(id_tipo_fase)

        tipo_fase = Tipo_Fase.get_tipo_fase_by_id(id_tipo_fase)
        tipos_items = Tipo_Item.get_tipos_items()
        tipos = tipo_fase.tipos_items
        tipos_items2 = []

        for tip in tipos:
            tipos_items2.append(tip.id_tipo_item)

        if request.method != 'PUT':  

            values = dict(id_tipo_fase=tipo_fase.id_tipo_fase, 
							nombre_tipo_fase=tipo_fase.nombre_tipo_fase, 
							descripcion=tipo_fase.descripcion,
							)
        
        return dict(pagina="editar_tipo_fase",values=values,
                        tipos_items=tipos_items, nom_proyecto=nom_proyecto,
                         tipos_items2=tipos_items2,nom_fase=nom_fase)


#-------------------------------------------------------------------------------

    @validate({'id_tipo_fase':Int(not_empty=True), 
				'nombre_tipo_fase':NotEmpty, 
				}, error_handler=editar_tipo_fase)	

#-------------------------------------------------------------------------------

    @expose()
    def put_tipo_fase(self, id_tipo_fase, nombre_tipo_fase, descripcion,
                       tipos_items, **kw):

        if id_tipo_fase is not None:
            id_tipo_fase=int(id_tipo_fase)

        tipo_fase = Tipo_Fase.get_tipo_fase_by_id(id_tipo_fase)

        if not isinstance(tipos_items, list):
			tipos_items = [tipos_items]
        tipos_items = [DBSession.query(Tipo_Item).get(tipo_item) for tipo_item
                                 in tipos_items]

        tipo_fase.nombre_tipo_fase = nombre_tipo_fase
        tipo_fase.descripcion = descripcion
        tipo_fase.tipos_items=tipos_items

        DBSession.flush()
        flash("Tipo de Fase modificada!")
        redirect('/tipo_fase/tipo_fase')

 ################################################################################

    @expose('saip2011.templates.tipo_fase.listar_tipo_fase')
    def listar_tipo_fase(self):
        """Lista tipos de fases 
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        tipos_fases = Tipo_Fase.get_tipo_fase()

        return dict(pagina="listar_tipo_fase",tipos_fases=tipos_fases,
                        nom_proyecto=nom_proyecto,nom_fase=nom_fase)

###############################################################################

    @expose('saip2011.templates.tipo_fase.listar_mis_tipos_items')
    def ver_tipos_items(self,id_tipo_fase):
        """Lista privilegios 
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        if id_tipo_fase is not None:
            id_tipo_fase=int(id_tipo_fase)

        tipo_fase=Tipo_Fase.get_tipo_fase_by_id(id_tipo_fase)

        values = dict(id_tipo_fase=tipo_fase.id_tipo_fase, 
				        nombre_tipo_fase=tipo_fase.nombre_tipo_fase, 
				        descripcion=tipo_fase.descripcion
				        )

        tipos =tipo_fase.tipos_items
        tipos_items = []

        for t in tipos:
            tipos_items.append(t)

        return dict(pagina="listar_mis_tipos_items",tipos_items=tipos_items,
                        nom_proyecto=nom_proyecto,nom_fase=nom_fase,
                        values=values)

###############################################################################


    @expose('saip2011.templates.tipo_fase.eliminar_tipo_fase')
    def eliminar_tipo_fase(self,id_tipo_fase, *args, **kw):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        if id_tipo_fase is not None:
            id_tipo_fase=int(id_tipo_fase)

        tipo_fase =Tipo_Fase.get_tipo_fase_by_id(id_tipo_fase)	

        values = dict(id_tipo_fase=tipo_fase.id_tipo_fase, 
						nombre_tipo_fase=tipo_fase.nombre_tipo_fase, 
						descripcion=tipo_fase.descripcion,
						)

        return dict(pagina="eliminar_tipo_fase",values=values,
                        nom_proyecto=nom_proyecto,nom_fase=nom_fase)

#-------------------------------------------------------------------------------

    @validate({'id_tipo_fase':Int(not_empty=True), 
				'nombre_tipo_fase':NotEmpty, 

				}, error_handler=eliminar_tipo_fase)	

#-------------------------------------------------------------------------------
    @expose()
    def post_delete_tipo_fase(self, id_tipo_fase, nombre_tipo_fase, descripcion,
                                     **kw):
	
        if id_tipo_fase is not None:
            id_tipo_fase=int(id_tipo_fase)

        Tipo_Fase.borrar_by_id(id_tipo_fase)
        DBSession.flush()
        flash("Tipo de Fase eliminada!")
        redirect('/tipo_fase')

 ################################################################################

    @expose('saip2011.templates.tipo_fase.agregar_tipo_fase')
    def agregar_tipo_fase(self,*args, **kw):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        tipos_items = Tipo_Item.get_tipos_items()

        return dict(pagina='agregar_tipo_fase',nom_proyecto=nom_proyecto,       
                            values=kw,tipos_items = tipos_items,
                            nom_fase=nom_fase)

#-------------------------------------------------------------------------------

    @validate({'nombre_tipo_fase':NotEmpty, 
                }, error_handler=agregar_tipo_fase)

#-------------------------------------------------------------------------------

    @expose()
    def post_tipo_fase(self, nombre_tipo_fase, tipos_items, descripcion,asmSelect0):
        
        if tipos_items is not None:
            if not isinstance(tipos_items, list):
                tipos_items = [tipos_items]
        tipos_items = [DBSession.query(Tipo_Item).get(tipo_item) for tipo_item 
                                                in tipos_items]

        tipo_fase = Tipo_Fase (nombre_tipo_fase=nombre_tipo_fase,
                    descripcion=descripcion,tipos_items=tipos_items)
  
        DBSession.add(tipo_fase)
        DBSession.flush()
        flash("tipo_fase agregada!")  
        redirect('/tipo_fase/tipo_fase')

 ################################################################################


