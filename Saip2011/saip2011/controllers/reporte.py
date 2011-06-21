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
        """Lista de reportes 
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        return dict(pagina='../reporte/reporte',nom_proyecto=nom_proyecto,nom_fase=nom_fase)
    
    @expose('saip2011.templates.reporte.relaciones')
    def relaciones (self):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        id_fase=int(Variables.get_valor_by_nombre("fase_actual"))
        items = Item.get_item_activados_by_fase(id_fase)
      
        return dict(pagina='../reporte/relaciones',items=items,nom_proyecto=nom_proyecto
                    ,nom_fase=nom_fase)

    @expose('saip2011.templates.reporte.ver_mis_padres')
    def ver_mis_padres (self, id_item):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        if id_item is not None:
            id_item=int(id_item)

        id_fase=int(Variables.get_valor_by_nombre("fase_actual"))
        items = Relaciones.get_mis_padres(id_item)
      
        return dict(pagina='../reporte/ver_mis_padres',items=items,nom_proyecto=nom_proyecto
                    ,nom_fase=nom_fase)

    @expose('saip2011.templates.reporte.ver_mis_hijos')
    def ver_mis_hijos (self, id_item):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        if id_item is not None:
            id_item=int(id_item)

        id_fase=int(Variables.get_valor_by_nombre("fase_actual"))
        hijos = Relaciones.get_mis_id_hijos(id_item)
        items=[]
        for hijo in hijos:
            h=Item.get_item_by_id(int(hijo))
            items.append(h)
      
        return dict(pagina='../reporte/ver_mis_hijos',items=items,nom_proyecto=nom_proyecto
                    ,nom_fase=nom_fase)

 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

