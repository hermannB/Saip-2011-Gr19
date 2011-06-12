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



class FaseController(BaseController):
    

################################################################################

    @expose('saip2011.templates.fase.listar_fase')
    def fase(self):
        """
        Menu para Fases
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        fases=Fase.get_fase_by_proyecto(int (Variables.get_valor_by_nombre
                                                ("proyecto_actual")) )
        return dict(pagina="listar_fase",fases=fases,nom_proyecto=nom_proyecto)
        #return dict(pagina="fase",nom_proyecto=nom_proyecto)

################################################################################
    
    @expose('saip2011.templates.fase.listar_fase')
    def listar_fase(self):
        """Lista fases 
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        #fases = Fase.get_fase()
        fases=Fase.get_fase_by_proyecto(int (Variables.get_valor_by_nombre
                                                ("proyecto_actual")) )
        return dict(pagina="listar_fase",fases=fases,nom_proyecto=nom_proyecto)

################################################################################

    @expose('saip2011.templates.fase.editar_fase')
    def editar_fase(self,id_fase,*args, **kw):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        tipos_fases = DBSession.query(Tipo_Fase).all()
        fase = DBSession.query(Fase).get(id_fase)
        tipos_items = DBSession.query(Tipo_Item).all()
        id_tipo_fase=fase.id_tipo_fase, 
        tipos = fase.tipos_items
        tipos_items2 = []
        for tip in tipos:
            tipos_items2.append(tip.id_tipo_item)

        if request.method != 'PUT':  
            values = dict(id_fase=fase.id_fase, 
                            nombre_fase=fase.nombre_fase, 
                            estado=fase.estado,
                            linea_base=fase.linea_base,
                            descripcion=fase.descripcion,
                            )

        return dict(pagina="editar_fase",values=values,tipos_fases=tipos_fases,
                        tipos_items=tipos_items,tipos_items2=tipos_items2,
                        id_tipo_fase=id_tipo_fase)

    @validate({'id_fase':Int(not_empty=True), 
                'nombre_fase':NotEmpty, 
                'id_tipo_fase':Int(not_empty=True), 
                #       'descripcion':NotEmpty
                }, error_handler=editar_fase)	

    @expose()
    def put_fase(self, id_fase, nombre_fase, id_tipo_fase, tipos_items,
                    descripcion, asmSelect0, **kw):
        fase = DBSession.query(Fase).get(int(id_fase))
        if not isinstance(tipos_items, list):
			tipos_items = [tipos_items]
        tipos_items = [DBSession.query(Tipo_Item).get(tipo_item) for tipo_item
                                 in tipos_items]

        fase.nombre_fase = nombre_fase
        fase.id_tipo_fase=id_tipo_fase
        fase.estado = fase.estado
        fase.linea_base = fase.linea_base
        fase.descripcion = descripcion
        fase.tipos_items=tipos_items

        DBSession.flush()
        flash("Fase modificada!")
        redirect('/fase/fase')

################################################################################

    @expose('saip2011.templates.fase.eliminar_fase')
    def eliminar_fase(self,id_fase, *args, **kw):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        fase2 = DBSession.query(Fase).get(id_fase)	
        values = dict(id_fase=fase2.id_fase, 
                        nombre_fase=fase2.nombre_fase, 
                        nombre_tipo_fase=fase2.nombre_tipo_fase, 
                        estado=fase2.estado,
                        descripcion=fase2.descripcion,
                        )

        return dict(pagina="eliminar_fase",values=values,
                        nom_proyecto=nom_proyecto)

    @validate({'id_fase':Int(not_empty=True), 
                'nombre_fase':NotEmpty, 
                'nombre_tipo_fase':NotEmpty, 
                #     'descripcion':NotEmpty
                }, error_handler=eliminar_fase)	

    @expose()
    def post_delete_fase(self, id_fase, nombre_fase,  nombre_tipo_fase, estado,
                                descripcion, **kw):

        DBSession.delete(DBSession.query(Fase).get(id_fase))
        DBSession.flush()
        flash("Fase eliminada!")
        redirect('/fase/fase')

################################################################################

    @expose('saip2011.templates.fase.agregar_fase')
    def agregar_fase(self, *args, **kw):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        tipos_fases = DBSession.query(Tipo_Fase).all()
        tipos_items = DBSession.query(Tipo_Item).all()
        return dict(pagina="agregar_fase",values=kw, tipos_fases=tipos_fases,
                        tipos_items=tipos_items,nom_proyecto=nom_proyecto)

    @validate({'nombre_fase':NotEmpty, 
                'id_tipo_fase':Int(not_empty=True), 
                #		'descripcion':NotEmpty
                }, error_handler=agregar_fase)

    @expose()
    def post_fase(self, nombre_fase, id_tipo_fase, tipos_items, descripcion,
                    asmSelect0):
        
        if id_tipo_fase is not None:
            id_tipo_fase = int(id_tipo_fase)
        if tipos_items is not None:
            if not isinstance(tipos_items, list):
                tipos_items = [tipos_items]
        tipos_items = [DBSession.query(Tipo_Item).get(tipo_item) for tipo_item 
                                                in tipos_items]
        fase = Fase (nombre_fase=nombre_fase, id_tipo_fase=id_tipo_fase, 
                    estado="nuevo", linea_base="abierta", 
                    descripcion=descripcion,tipos_items=tipos_items,
                    proyecto=0,orden=0)
  
        DBSession.add(fase)
        flash("Fase agregada!")  
        redirect('/fase/fase')

################################################################################
  
    @expose('saip2011.templates.item.menu_item')
    def seleccionar_fase(self,id_fase,*kw,**args):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        proy_act=int (Variables.get_valor_by_nombre("proyecto_actual"))
        Variables.set_valor_by_nombre("fase_actual",id_fase)
        items = Item.get_item_proy_fase( proy_act, id_fase)
        return dict(pagina="listar_item",items=items,nom_proyecto=nom_proyecto)

        
  

