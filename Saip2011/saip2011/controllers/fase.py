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

    @expose('saip2011.templates.fase.fase')
    def fase(self,start=0,end=5,indice=None,texto=""):
        """
        Menu para Fases
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        paginado = 5
        if start <> 0:
            end=int(start.split('=')[1]) #obtiene el fin de pagina
            start=int(start.split('&')[0]) #obtiene el inicio de pagina
        #print start,end
        #total = len(Fase.get_fase_by_proyecto(int (Variables.get_valor_by_nombre
         #                                       ("proyecto_actual")) ))
        pagina_actual = ((start % end) / paginado) + 1
        if ((start % end) % paginado) <> 0:
             pagina_actual = pagina_actual + 1
                      
        if indice  <> None and texto <> "":  
            fases = Fase.get_fase_by_proyecto_por_filtro(int (Variables.get_valor_by_nombre
                                                ("proyecto_actual")),indice,texto)
            total = len(fases)
        else:   
            fases, total = Fase.get_fase_by_proyecto_por_pagina(int (Variables.get_valor_by_nombre
                                                            ("proyecto_actual")),start,end )
            #fases = Fase.get_fase_by_proyecto(int (Variables.get_valor_by_nombre
            #                                    ("proyecto_actual")) )
            #total = len(fases)

        lista = ['nombre','descripcion']


        return dict(pagina="fase",fases=fases,nom_proyecto=nom_proyecto
                        ,nom_fase=nom_fase,inicio=start,fin=end,paginado=paginado,
                        pagina_actual=pagina_actual,total=total,param="/fase/fase",
                        lista=lista)

################################################################################
    
    @expose('saip2011.templates.fase.listar_fase')
    def listar_fase(self):
        """Lista fases 
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        fases=Fase.get_fase_by_proyecto(int (Variables.get_valor_by_nombre
                                                ("proyecto_actual")) )

        return dict(pagina="listar_fase",fases=fases,nom_proyecto=nom_proyecto
                        ,nom_fase=nom_fase)


 ################################################################################

    @expose('saip2011.templates.fase.editar_fase')
    def editar_fase(self,id_fase,*args, **kw):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        if id_fase is not None:
            id_fase=int(id_fase)

        tipos_fases = Tipo_Fase.get_tipo_fases()
        fase = Fase.get_fase_by_id(id_fase)
        tipos_items = Tipo_Item.get_tipos_items()
        id_tipo_fase=int(fase.id_tipo_fase)

        lista=[]
        lista.append(id_tipo_fase)
        tipos = fase.tipos_items

        tipos_items2 = []
        for tip in tipos:
            tipos_items2.append(tip.id_tipo_item)

        if request.method != 'PUT':  
            values = dict(id_fase=fase.id_fase, 
                            nombre_fase=fase.nombre_fase, 
                            descripcion=fase.descripcion,
                            )

        return dict(pagina="editar_fase",values=values,tipos_fases=tipos_fases,
                        tipos_items=tipos_items,tipos_items2=tipos_items2,
                        lista=lista,nom_fase=nom_fase,
                        nom_proyecto= nom_proyecto )

#-------------------------------------------------------------------------------

    @validate({'id_fase':Int(not_empty=True), 
                'nombre_fase':NotEmpty, 
                'id_tipo_fase':Int(not_empty=True), 
                }, error_handler=editar_fase)	

#-------------------------------------------------------------------------------

    @expose('saip2011.templates.fase.editar_fase')
    def put_fase(self, id_fase, nombre_fase, id_tipo_fase, tipos_items,
                    descripcion, asmSelect0,  **kw):

        if id_fase is not None:
            id_fase=int(id_fase)

        if id_tipo_fase is not None:
            id_tipo_fase=int(id_tipo_fase)

        fase =Fase.get_fase_by_id(id_fase)
        nombres=Fase.get_nombres_by_id(fase.proyecto)
        nombres.remove(fase.nombre_fase)
        
        if not isinstance(tipos_items, list):
			tipos_items = [tipos_items]
        tipos_items = [DBSession.query(Tipo_Item).get(tipo_item) for tipo_item
                                 in tipos_items]

        if nombre_fase not in nombres:
            fase.nombre_fase = nombre_fase
            fase.id_tipo_fase=id_tipo_fase
            fase.estado = fase.estado
            fase.linea_base = fase.linea_base
            fase.descripcion = descripcion
            fase.tipos_items=tipos_items

            DBSession.flush()
            flash("Fase modificada!")
            redirect('/fase/fase')
    
        else:
            nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
            nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

            id_tipo_fase=fase.id_tipo_fase
            tipos_fases = Tipo_Fase.get_tipo_fases()
            tipos = fase.tipos_items

            lista=[]
            lista.append(id_tipo_fase)
            tipos = fase.tipos_items

            tipos_items2 = []
            for tip in tipos:
                tipos_items2.append(tip.id_tipo_item)

            values = dict(id_fase=id_fase, 
                            nombre_fase=nombre_fase, 
                            descripcion=descripcion,
                            )
            flash("El nombre de fase solicitado ya existe!")

            return dict(pagina="editar_fase",values=values,
                                tipos_fases=tipos_fases,tipos_items=tipos_items,
                                tipos_items2=tipos_items2,lista=lista, 
                                id_tipo_fase=id_tipo_fase,nom_fase=nom_fase,
                                nom_proyecto= nom_proyecto )

################################################################################

    @expose('saip2011.templates.fase.eliminar_fase')
    def eliminar_fase(self,id_fase, *args, **kw):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        if id_fase is not None:
            id_fase=int(id_fase)

        fase2 = Fase.get_fase_by_id(id_fase)
        values = dict(id_fase=fase2.id_fase, 
                        nombre_fase=fase2.nombre_fase, 
                        nombre_tipo_fase=fase2.nombre_tipo_fase, 
                        estado=fase2.estado,
                        descripcion=fase2.descripcion,
                        )

        return dict(pagina="eliminar_fase",values=values,
                        nom_proyecto=nom_proyecto,nom_fase=nom_fase)

#-------------------------------------------------------------------------------

    @validate({'id_fase':Int(not_empty=True), 
                'nombre_fase':NotEmpty, 
                'nombre_tipo_fase':NotEmpty, 
                #     'descripcion':NotEmpty
                }, error_handler=eliminar_fase)	

#-------------------------------------------------------------------------------

    @expose()
    def post_delete_fase(self, id_fase, nombre_fase,  nombre_tipo_fase, estado,
                                descripcion, **kw):

        Fase.borrar_by_id(id_fase)
        DBSession.flush()

        flash("Fase eliminada!")
        redirect('/fase/fase')

################################################################################

    @expose('saip2011.templates.fase.agregar_fase')
    def agregar_fase(self, *args, **kw):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        tipos_fases = Tipo_Fase.get_tipo_fases()
        tipos_items = Tipo_Item.get_tipos_items()

        return dict(pagina="agregar_fase",values=kw, tipos_fases=tipos_fases,
                        tipos_items=tipos_items,nom_proyecto=nom_proyecto
                        ,nom_fase=nom_fase)

#-------------------------------------------------------------------------------

    @validate({'nombre_fase':NotEmpty, 
                'id_tipo_fase':Int(not_empty=True), 
                }, error_handler=agregar_fase)

#-------------------------------------------------------------------------------

    @expose('saip2011.templates.fase.agregar_fase')
    def post_fase(self, nombre_fase, id_tipo_fase, tipos_items, descripcion,
                    asmSelect0):
        proyecto=int(Variables.get_valor_by_nombre("proyecto_actual"))
        nombres=Fase.get_nombres_by_id(proyecto)

        if not isinstance(nombres, list):
            nombres = [nombres]

        if nombre_fase not in nombres:

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
            DBSession.flush()
            flash("Fase agregada!")  
            redirect('/fase/fase')

        else:
            nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
            nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

            tipos_fases = Tipo_Fase.get_tipo_fases()
            tipos_items = Tipo_Item.get_tipos_items()

            values = dict(nombre_fase=nombre_fase, 
                            descripcion=descripcion,
                            )
            flash("Nombre de Fase es repetido!")
            return dict(pagina="agregar_fase",values=values, tipos_fases=tipos_fases,
                            tipos_items=tipos_items,nom_proyecto=nom_proyecto
                            ,nom_fase=nom_fase)

################################################################################
  
    @expose('saip2011.templates.item.menu_item')
    def seleccionar_fase(self,id_fase,start=0,end=5,indice=None,texto="",*kw,**args):

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
        param = "/fase/seleccionar_fase?id_fase=%s" % id_fase
        items = Item.get_item_activados_by_fase(id_fase)
        return dict(pagina="menu_item",items=items,nom_proyecto=nom_proyecto
                        ,nom_fase=nom_fase,paginado=paginado,inicio=start,
                        fin=end,pagina_actual=pagina_actual,total=total,
                        param=param,lista=lista)

################################################################################
        
  

