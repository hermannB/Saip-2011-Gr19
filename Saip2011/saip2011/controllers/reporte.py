# -*- coding: utf-8 -*-
"""Reporte Controller"""

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
from saip2011.model.campos import Campos
from saip2011.model.relaciones import Relaciones
from saip2011.model.linea_base import Linea_Base
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



class ReporteController(BaseController):
    
    @expose('saip2011.templates.reporte.reporte')
    def reporte(self):
        """
        Lista de reportes 
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")
        
        return dict(pagina="reporte",nom_proyecto=nom_proyecto,nom_fase=nom_fase)
    print reporte.__doc__


 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @expose('saip2011.templates.reporte.item2')
    def item2(self,start=0,end=5,indice=None,texto=""):
        """
        Menu para Item
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        paginado = 5
        if start <> 0:
            end=int(start.split('=')[1]) #obtiene el fin de pagina
            start=int(start.split('&')[0]) #obtiene el inicio de pagina
        #print start,end
        
        pagina_actual = ((start % end) / paginado) + 1
        if ((start % end) % paginado) <> 0:
             pagina_actual = pagina_actual + 1
                         
        if indice  <> None and texto <> "":  
            fases=Fase.get_fase_by_proyecto_por_filtro(int (Variables.get_valor_by_nombre
                                                ("proyecto_actual")), indice,texto )
            total = len(fases)
        else:   
            fases,total=Fase.get_fase_by_proyecto_por_pagina(int (Variables.get_valor_by_nombre
                                                ("proyecto_actual")), start,end )

            #total = len(Fase.get_fase_by_proyecto(int (Variables.get_valor_by_nombre
             #                                   ("proyecto_actual")) ))

        lista = ['nombre','descripcion']
        
        return dict(pagina="listar_fases2",fases=fases,nom_proyecto=nom_proyecto
                                ,nom_fase=nom_fase,inicio=start,fin=end,
                                pagina_actual=pagina_actual,paginado=paginado,
                                total=total,param="../reporte/item2",lista=lista)
    print item2.__doc__

###################################################################################


    @expose('saip2011.templates.reporte.listar_fases2')
    def listar_fases2(self):
        """Lista las fases. 
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        fases=Fase.get_fase_by_proyecto(int (Variables.get_valor_by_nombre
                                                ("proyecto_actual")) )

        return dict(pagina="listar_fases2",fases=fases,nom_proyecto=nom_proyecto
                        ,nom_fase=nom_fase)

    print listar_fases2.__doc__


 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    @expose('saip2011.templates.reporte.menu_item')
    def seleccionar_fase(self,id_fase,start=0,end=5,indice=None,texto="",*kw,**args):
        """
        Permite seleccionar una fase.
        """

        if id_fase is not None:
            id_fase=int(id_fase)

        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        proy_act=int (Variables.get_valor_by_nombre("proyecto_actual"))

        Variables.set_valor_by_nombre("fase_actual",id_fase)
        fase=Fase.get_fase_by_id(id_fase)
        Variables.set_valor_by_nombre("nombre_fase_actual",fase.nombre_fase)
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        #items = Item.get_item_proy_fase( proy_act, id_fase)
        
        #id_fase=int(Variables.get_valor_by_nombre("fase_actual"))
        #items = Item.get_item_activados_by_fase(id_fase)
        
        paginado = 5
        if start <> 0:
            end=int(start.split('=')[1]) #obtiene el fin de pagina
            start=int(start.split('&')[0]) #obtiene el inicio de pagina
        #print start,end
        #total = len(Privilegios.get_privilegios())
        pagina_actual = ((start % end) / paginado) + 1
        if ((start % end) % paginado) <> 0:
             pagina_actual = pagina_actual + 1
        
        if indice  <> None and texto <> "":  
            items = Item.get_item_activados_by_fase_por_filtro(id_fase,indice,texto)
            total = len(privilegios)
        else:   
            items = Item.get_item_activados_by_fase_por_pagina(id_fase,start,end)
            total = len(Item.get_item_activados_by_fase(id_fase))

        lista = ['nombre','descripcion']
        param = "../reporte/seleccionar_fase?id_fase=%s" % id_fase
        items = Item.get_item_proy_fase( proy_act, id_fase)
        return dict(pagina="../reporte/listar_item.html",items=items,nom_proyecto=nom_proyecto
                        ,nom_fase=nom_fase,paginado=paginado,inicio=start,
                        fin=end,pagina_actual=pagina_actual,total=total,
                        param=param,lista=lista)
    print seleccionar_fase.__doc__

##################################################################################################

    @expose('saip2011.templates.reporte.menu_item')
    def ver_mis_padres (self, id_item):
        """
        Permite listar los padres de un item dado.
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        if id_item is not None:
            id_item=int(id_item)

        id_fase=int(Variables.get_valor_by_nombre("fase_actual"))
        items = Relaciones.get_mis_padres(id_item)
        for it in items:
            if (it.estado_oculto=="Activo"):
                items.remove(it)
      
        return dict(pagina='ver_mis_padres.html',items=items,nom_proyecto=nom_proyecto
                    ,nom_fase=nom_fase)
    print ver_mis_padres.__doc__
###################################################################################################


    @expose('saip2011.templates.reporte.menu_item')
    def ver_mis_hijos (self, id_item):
        """
        Permite visualizar los hijos de un item.
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        if id_item is not None:
            id_item=int(id_item)

        id_fase=int(Variables.get_valor_by_nombre("fase_actual"))
        hijos = Relaciones.get_mis_id_hijos(id_item)
        items=[]
        for hijo in hijos:
            h=Item.get_item_by_id(int(hijo))
            if (h.estado_oculto=="Activo"):
                items.append(h)
      
        return dict(pagina='ver_mis_hijos.html',items=items,nom_proyecto=nom_proyecto
                    ,nom_fase=nom_fase)
    print ver_mis_hijos.__doc__
#####################################################################################################

    @expose('saip2011.templates.reporte.impacto')
    def impacto (self, id_item):
        """
        Permite visualizar un reporte de impacto.
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        if id_item is not None:
            id_item=int(id_item)
        item=Item.get_item_by_id(id_item)
        items = Relaciones.get_sucesores(id_item)

        impacto=item.complejidad
        for it in items:
            if (it.estado_oculto=="Activo"):
                impacto+=it.complejidad
    
        values = dict(id_item=item.id_item, 
	                   nombre_item=item.nombre_item,
	                   codigo_item=item.codigo_item,  
		               nombre_tipo_item=item.nombre_tipo_item,
                       impacto=impacto
		                )

      
        return dict(pagina='impacto.html',values=values,nom_proyecto=nom_proyecto
                    ,nom_fase=nom_fase)
    print impacto.__doc__
###################################################################################

    @expose('saip2011.templates.reporte.imagen')
    def arbol (self, id_item):
        """
        Permite visualizar las relaciones de un item dado.
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        if id_item is not None:
            id_item=int(id_item)
        item=Item.get_item_by_id(id_item)
        items = Item.get_item_activados()
        Relaciones.matriz_relaciones(id_item)

        values = dict(id_item=item.id_item, 
	                   nombre_item=item.nombre_item,
	                   codigo_item=item.codigo_item,  
		               nombre_tipo_item=item.nombre_tipo_item

		                )




      
        return dict(pagina='imagen.html',values=values,nom_proyecto=nom_proyecto
                    ,nom_fase=nom_fase)
    print arbol.__doc__


 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
