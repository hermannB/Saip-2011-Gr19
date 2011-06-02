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



class FaseController(BaseController):
    

 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    @expose('saip2011.templates.fase.fase')
    def fase(self):
        """
           Menu para Fases
        """
        return dict(pagina="fase")
        
    @expose('saip2011.templates.fase.listar_fase')
    def listar_fase(self):
        """Lista fases 
        """
        fases = Fase.get_fase()
        return dict(pagina="listar_fase",fases=fases)

    @expose('saip2011.templates.fase.editar_fase')
    def editar_fase(self,id_fase,*args, **kw):
        tipos_fases = DBSession.query(Tipo_Fase).all()
        fase = DBSession.query(Fase).get(id_fase)

        if request.method != 'PUT':  
            values = dict(id_fase=fase.id_fase, 
                            nombre_fase=fase.nombre_fase, 
                            id_tipo_fase=fase.id_tipo_fase, 
                            estado=fase.estado,
                            linea_base=fase.linea_base,
                            descripcion=fase.descripcion,
                            )

        return dict(pagina="editar_fase",values=values,tipos_fases=tipos_fases)

    @validate({'id_fase':Int(not_empty=True), 
                'nombre_fase':NotEmpty, 
                'id_tipo_fase':Int(not_empty=True), 
                'estado':NotEmpty, 
                #       'descripcion':NotEmpty
                }, error_handler=editar_fase)	

    @expose()
    def put_fase(self, id_fase, nombre_fase, id_tipo_fase, estado, linea_base, descripcion, **kw):
        fase = DBSession.query(Fase).get(int(id_fase))

        fase.nombre_fase = nombre_fase
        fase.id_tipo_fase=id_tipo_fase
        fase.estado = estado
        fase.linea_base = linea_base
        fase.descripcion = descripcion

        DBSession.flush()
        flash("Fase modificada!")
        redirect('/fase')

    @expose('saip2011.templates.fase.eliminar_fase')
    def eliminar_fase(self,id_fase, *args, **kw):
        fase2 = DBSession.query(Fase).get(id_fase)	
        values = dict(id_fase=fase2.id_fase, 
                        nombre_fase=fase2.nombre_fase, 
                        nombre_tipo_fase=fase2.nombre_tipo_fase, 
                        estado=fase2.estado,
                        linea_base=fase2.linea_base,
                        descripcion=fase2.descripcion,
                        )

        return dict(pagina="eliminar_fase",values=values)

    @validate({'id_fase':Int(not_empty=True), 
                'nombre_fase':NotEmpty, 
                'nombre_tipo_fase':NotEmpty, 
                'estado':NotEmpty, 
                #     'descripcion':NotEmpty
                }, error_handler=eliminar_fase)	

    @expose()
    def post_delete_fase(self, id_fase, nombre_fase,  nombre_tipo_fase, estado, linea_base, descripcion, **kw):

        DBSession.delete(DBSession.query(Fase).get(id_fase))
        DBSession.flush()
        flash("Fase eliminada!")
        redirect('/fase')

    @expose('saip2011.templates.fase.agregar_fase')
    def agregar_fase(self, *args, **kw):
        tipos_fases = DBSession.query(Tipo_Fase).all()
        return dict(pagina="agregar_fase",values=kw, tipos_fases=tipos_fases)

    @validate({'nombre_fase':NotEmpty, 
                'id_tipo_fase':Int(not_empty=True), 
                'estado':NotEmpty,
                'linea_base':NotEmpty,
                #		'descripcion':NotEmpty
                }, error_handler=agregar_fase)

    @expose()
    def post_fase(self, nombre_fase, id_tipo_fase, estado ,linea_base, descripcion):
        if id_tipo_fase is not None:
            id_tipo_fase = int(id_tipo_fase)
        
        fase = Fase (nombre_fase=nombre_fase, id_tipo_fase=id_tipo_fase, 
                    estado=estado, linea_base=linea_base, descripcion=descripcion)
  
        DBSession.add(fase)
        flash("Fase agregada!")  
        redirect('./fase')
  
  
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

