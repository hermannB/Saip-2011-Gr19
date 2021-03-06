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
import string



class ProyectoController(BaseController):

################################################################################

    @expose('saip2011.templates.proyecto.proyecto')
    def proyecto(self,start=0,end=5,indice=None,texto=""):
        """Lista proyectos 
        """
        proyectos=""

        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        usuario=Usuario.get_user_by_alias(request.identity['repoze.who.userid'])
        rol=usuario.roles[0]

        ############################
        paginado = 5
        if start <> 0:
            end=int(start.split('=')[1]) #obtiene el fin de pagina
            start=int(start.split('&')[0]) #obtiene el inicio de pagina
        #print start,end
        
        pagina_actual = ((start % end) / paginado) + 1
        if ((start % end) % paginado) <> 0:
             pagina_actual = pagina_actual + 1
         
        #roles = Rol.get_roles_por_pagina(start,end)
        ###########################
        
        lista = ['nombre','descripcion']

        if rol.nombrerol == "Administrador":
            #proyectos = Proyecto.get_proyecto_por_pagina(start,end)
            if indice  <> None and texto <> "":  
                proyectos = Proyecto.get_proyectos_por_filtro(indice,texto)
                total = len(proyectos)
            else:   
                proyectos = Proyecto.get_proyectos_por_pagina(start,end)
                total = len(Proyecto.get_proyectos())
            
            return dict(pagina="proyecto",proyectos=proyectos,
                            nom_proyecto=nom_proyecto,nom_fase=nom_fase,
                            inicio=start,fin=end,paginado=paginado,
                            pagina_actual=pagina_actual,total=total,
                            lista=lista,param="/proyecto/proyecto")
        else:
            if indice  <> None and texto <> "":  
                proyectos = Proyecto.get_proyectos_by_equipo_desarrollo_por_filtro(usuario.idusuario,
                                                                                   indice,texto)
                total = len(proyectos)
            else:   
                proyectos,total = Proyecto.get_proyectos_by_equipo_desarrollo_por_pagina(usuario.idusuario,
                                                                                   start,end)
                #total = len(Proyecto.get_proyectos_by_equipo_desarrollo(usuario.idusuario))
            
                        
            #total = len(proyectos)

        return dict(pagina="proyecto",proyectos=proyectos,
                        nom_proyecto=nom_proyecto,nom_fase=nom_fase,
                        inicio=start,fin=end,paginado=paginado,
                        pagina_actual=pagina_actual,total=total,
                        lista=lista,param="/proyecto/proyecto")


################################################################################
        
    @expose('saip2011.templates.proyecto.listar_proyecto')
    def listar_proyecto(self):
        """Lista proyectos 
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")		

        proyectos = Proyecto.get_proyecto()

        return dict(pagina="listar_proyecto",proyectos=proyectos,
                        nom_proyecto=nom_proyecto,nom_fase=nom_fase)

################################################################################

    @expose('saip2011.templates.proyecto.listar_mis_fases')
    def ver_fases(self,id_proyecto):
        """Lista privilegios 
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        if id_proyecto is not None:
            id_proyecto=int(id_proyecto)

        proyecto=Proyecto.get_proyecto_by_id(id_proyecto)

        values = dict(id_proyecto=proyecto.id_proyecto, 
				        nombre_proyecto=proyecto.nombre_proyecto, 
				        descripcion=proyecto.descripcion
				        )

        fas = Fase.get_fase_by_proyecto(int (id_proyecto) )
        fases = []
        for f in fas:
            fases.append(f)

        return dict(pagina="listar_mis_fases",fases=fases,
                        nom_proyecto=nom_proyecto,nom_fase=nom_fase,
                        values=values)

###############################################################################

    @expose('saip2011.templates.proyecto.listar_mis_tipos_items')
    def ver_tipos_items(self,id_fase):
        """Lista privilegios 
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        if id_fase is not None:
            id_fase=int(id_fase)

        fase=Fase.get_fase_by_id(id_fase)

        values = dict(id_fase=fase.id_fase, 
				        nombre_fase=fase.nombre_fase, 
				        descripcion=fase.descripcion
				        )

        tipos =fase.tipos_items
        tipos_items = []
        for t in tipos:
            tipos_items.append(t)

        return dict(pagina="listar_mis_tipos_items",tipos_items=tipos_items,
                        nom_proyecto=nom_proyecto,nom_fase=nom_fase,
                        values=values)

###############################################################################

    @expose('saip2011.templates.proyecto.listar_mis_campos')
    def ver_campos(self,id_tipo_item):
        """Lista  
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        if id_tipo_item is not None:
            id_tipo_item=int(id_tipo_item)

        tipo_item=Tipo_Item.get_tipo_item_by_id(id_tipo_item)

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


    @expose('saip2011.templates.proyecto.ingresar_proyecto')
    def ingresar_proyecto(self):
        """lista de los  proyectos del usuario
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")	
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")	

        usuario=Usuario.get_user_by_alias(request.identity['repoze.who.userid'])
        proy = Proyecto.get_proyectos()
        proyectos = []
        miembros=Equipo_Desarrollo.get_miembros_by_usuario(usuario.idusuario)

        for miembro in miembros:
            for p in proy:
                if (miembro.proyecto == p.id_proyecto):
                    proyectos.append(p)

        return dict(pagina="ingresar_proyecto",proyectos=proyectos,
                    nom_proyecto=nom_proyecto,nom_fase=nom_fase)

#-------------------------------------------------------------------------------

    @expose()
    def ingresar(self,id_proyecto):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")

        usuario=Usuario.get_user_by_alias( request.identity['repoze.who.userid'])

        if id_proyecto is not None:
            id_proyecto=int(id_proyecto)

        proyecto=Proyecto.get_proyecto_by_id(id_proyecto)

        Variables.set_valor_by_nombre("fase_actual",0)
        Variables.set_valor_by_nombre("proyecto_actual",proyecto.id_proyecto)
        Variables.set_valor_by_nombre("nombre_proyecto_actual",
                                            proyecto.nombre_proyecto)

        miembros=Equipo_Desarrollo.get_miembros_by_proyecto(proyecto.id_proyecto)
        rol=""
        for miembro in miembros:
            if ( miembro.idusuario == usuario.idusuario ):
                temp=int (Variables.get_valor_by_nombre("rol_anterior"))
                if  temp == 0:		
                    Variables.set_valor_by_nombre("rol_anterior",
                                                    usuario.roles[0].idrol)

                Variables.set_valor_by_nombre("rol_actual",miembro.idrol)
                rol=Rol.get_rol_by_id(miembro.idrol)
                usuario.roles=[]

                DBSession.flush()
                usuario.roles.append(rol)
                DBSession.flush()
                break;
        redirect('/')

################################################################################

    @expose('saip2011.templates.proyecto.agregar_proyecto')
    def agregar_proyecto(self, *args, **kw):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        usuarios = Usuario.get_usuarios()
        tipos_fases = Tipo_Fase.get_tipo_fases()	

        return dict(pagina="agregar_proyecto",values=kw, tipos_fases=tipos_fases,
                         usuarios=usuarios,nom_proyecto=nom_proyecto
                        ,nom_fase=nom_fase)

#-------------------------------------------------------------------------------
    
    @validate({'nombre_proyecto':NotEmpty, 
				'idusuario':Int(not_empty=True), 
				'tipos_fases':NotEmpty,
				}, error_handler=agregar_proyecto)


#-------------------------------------------------------------------------------
    @expose('saip2011.templates.fase.fase')
    def post_proyecto(self, nombre_proyecto, idusuario, tipos_fases, asmSelect0,
                            descripcion,start=0,end=5,indice=None,texto=""):

        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        nombres=Proyecto.get_nombres()

        if not isinstance(nombres, list):
            nombres = [nombres]

        if nombre_proyecto not in nombres:
            if idusuario is not None:
                idusuario = int(idusuario)

            if tipos_fases is not None:
                if not isinstance(tipos_fases, list):
                    tipos_fases = [tipos_fases]
    
                tipos_fases = [DBSession.query(Tipo_Fase).get(tipo_fase) 
                                    for tipo_fase in tipos_fases]

            proyecto = Proyecto (nombre_proyecto=nombre_proyecto, 
                                    idusuario=idusuario, 
                                    descripcion=descripcion, 
                                    tipos_fases=tipos_fases,
                                    estado ="Desactivado")
            DBSession.add(proyecto)
            DBSession.flush()

            proy=int(Proyecto.get_ultimo_id())
            cant=1
            lista=[]
            for tipo_fase in tipos_fases:
                fase = Fase (nombre_fase=tipo_fase.nombre_tipo_fase, 
                                id_tipo_fase=tipo_fase.id_tipo_fase, 
                                estado ="Nuevo",proyecto=proy,
                                orden=cant,linea_base="Abierta", 
                                descripcion=tipo_fase.descripcion)

                DBSession.add(fase)
                DBSession.flush()
                lista.append(fase)
                cant+=1

            nom="Lider Proyecto"
            mirol=Rol.get_rol_by_nombre(nom)
            fases2=Fase.get_fase_by_proyecto(proy)
            equipo = Equipo_Desarrollo(proyecto=Proyecto.get_ultimo_id(), 
                                        idusuario=idusuario, 
                                        idrol=mirol.idrol,fases=fases2)

            DBSession.add(equipo)
            DBSession.flush()


            fases,len_fases = Fase.get_fase_by_proyecto_por_pagina(proy,start,end)


            ############
            paginado = 5
            if start <> 0:
                end=int(start.split('=')[1]) #obtiene el fin de pagina
                start=int(start.split('&')[0]) #obtiene el inicio de pagina
            #print start,end
            total = len(Fase.get_fase_by_proyecto(proy))
            pagina_actual = ((start % end) / paginado) + 1
            if ((start % end) % paginado) <> 0:
                pagina_actual = pagina_actual + 1
             
            #roles = Fase.get_fase_by_proyecto_por_pagina(proy,start,end)
            ###########
            param="/fase/fase"
            flash("Proyecto Agregado!")  
            return dict(pagina="../fase/fase", fases=fases,
                                nom_proyecto=nom_proyecto,nom_fase=nom_fase,
                                inicio=start,fin=end,paginado=paginado,
                                pagina_actual=pagina_actual,total=total,
                                param=param)

        else:
            nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
            nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

            usuarios = Usuario.get_usuarios()
            tipos_fases = Tipo_Fase.get_tipo_fases()	

            flash("Nombre del Proyecto ya existe!")  
            redirect('../proyecto/agregar_proyecto')

################################################################################

    @expose('saip2011.templates.proyecto.editar_proyecto')
    def editar_proyecto(self, id_proyecto, *args, **kw):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        if id_proyecto is not None:
            id_proyecto=int(id_proyecto)

        usuarios = Usuario.get_usuarios()
        tipos_fases = Tipo_Fase.get_tipo_fases()	
        proyecto = Proyecto.get_proyecto_by_id(id_proyecto)

        usuario2 = Usuario.get_user_by_id(int(proyecto.idusuario))
        
        tipos = proyecto.tipos_fases

        tipos_fases2 = []
        for tip in tipos:
            tipos_fases2.append(tip.id_tipo_fase)

        values = dict(id_proyecto=proyecto.id_proyecto, 
						nombre_proyecto=proyecto.nombre_proyecto, 
						descripcion=proyecto.descripcion, 
						idusuario=proyecto.idusuario
						)
                      
        values.update(kw)

        return dict(pagina="editar_proyecto",values=values, usuarios=usuarios,
                     tipos_fases=tipos_fases, tipos_fases2=tipos_fases2,
                    usuario2=usuario2, nom_proyecto=nom_proyecto,
                    nom_fase=nom_fase)

#-------------------------------------------------------------------------------

    @validate({'id_proyecto':Int(not_empty=True), 
				'nombre_proyecto':NotEmpty, 
				'tipos_fases':NotEmpty,
				'idusuario':Int(not_empty=True)
               }, error_handler=editar_proyecto)

#-------------------------------------------------------------------------------

    @expose('saip2011.templates.fase.listar_fase')
    def put_proyecto(self, id_proyecto, nombre_proyecto, idusuario, descripcion,
                         asmSelect0, tipos_fases,**kw):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        if id_proyecto is not None:
            id_proyecto=int(id_proyecto)

        if idusuario is not None:
            idusuario=int(idusuario)

        nombres=Proyecto.get_nombres()
        proyecto = DBSession.query(Proyecto).get(id_proyecto)

        if not isinstance(nombres, list):
            nombres = [nombres]
        nombres.remove(proyecto.nombre_proyecto)

        if nombre_proyecto not in nombres:

            miembro=Equipo_Desarrollo.get_miembro_by_usuario_by_proyecto(
                        proyecto.idusuario,proyecto.id_proyecto)

            id_miembro=miembro.id_equipo
            Equipo_Desarrollo.borrar_by_id(id_miembro)
            DBSession.flush()

            fases=Fase.get_fase_by_proyecto(proyecto.id_proyecto)

            for fase in fases:
			    Fase.borrar_by_id(fase.id_fase)
			    DBSession.flush()

            if not isinstance(tipos_fases, list):
			    tipos_fases = [tipos_fases]
            tipos_fases = [DBSession.query(Tipo_Fase).get(tipo_fase) 
                                for tipo_fase in tipos_fases]

            cant=1
            for tipo_fase in tipos_fases:
                fase = Fase (nombre_fase=tipo_fase.nombre_tipo_fase, 
                                id_tipo_fase=tipo_fase.id_tipo_fase, estado ="Nuevo", 
							    proyecto=proyecto.id_proyecto,orden=cant,
                                linea_base="Abierta", 
                                descripcion=tipo_fase.descripcion)

                DBSession.add(fase)
                DBSession.flush()
                cant+=1

            proyecto.idusuario = idusuario
            proyecto.nombre_proyecto=nombre_proyecto
            proyecto.descripcion = descripcion
            proyecto.tipos_fases = tipos_fases
            proyecto.estado="Desactivado"

            DBSession.flush()

            fases = Fase.get_fase_by_proyecto(Proyecto.get_ultimo_id())
            nom="Lider Proyecto"
            mirol=Rol.get_rol_by_nombre(nom)

            equipo = Equipo_Desarrollo(proyecto=Proyecto.get_ultimo_id(), 
                                        idusuario=idusuario, 
						                idrol=mirol.idrol,fases=fases)
            DBSession.add(equipo)
            DBSession.flush()
            fases = Fase.get_fase_by_proyecto(proyecto.id_proyecto)

            flash("Proyecto Modificado!")  
            return dict(pagina="/fase/listar_fase", fases=fases,
                            nom_proyecto=nom_proyecto,nom_fase=nom_fase)
        else:

            flash("nombre proyecto repetido!")  
            redirect('/proyecto/editar_proyecto?id_proyecto=%d' % id_proyecto)
        

################################################################################


    @expose('saip2011.templates.proyecto.eliminar_proyecto')
    def eliminar_proyecto(self,id_proyecto, *args, **kw):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        if id_proyecto is not None:
            id_proyecto=int(id_proyecto)

        proyecto = DBSession.query(Proyecto).get(id_proyecto)	

        values = dict(id_proyecto=proyecto.id_proyecto, 
						nombre_proyecto=proyecto.nombre_proyecto, 
						descripcion=proyecto.descripcion,
						lider_equipo=proyecto.lider_equipo,
						tipos_fases=proyecto.tipos_fases
						)

        return dict(pagina="eliminar_proyecto",values=values,
                        nom_proyecto=nom_proyecto,nom_fase=nom_fase)

#-------------------------------------------------------------------------------

    @validate({'id_proyecto':Int(not_empty=True), 
				'nombre_proyecto':NotEmpty, 
				'tipos_fases':NotEmpty,
				}, error_handler=eliminar_proyecto)	

#-------------------------------------------------------------------------------

    @expose()
    def post_delete_proyecto(self, id_proyecto, nombre_proyecto, descripcion, 
                                tipos_fases, **kw):

        if id_proyecto is not None:
            id_proyecto=int(id_proyecto)

        proyecto = Proyecto.get_proyecto_by_id(id_proyecto)
        miembros=Equipo_Desarrollo.get_miembros_by_proyecto(proyecto.idusuario)

        for miembro in miembros:
            id_miembro=miembro.id_equipo
            Equipo_Desarrolloborrar_by_id(id_miembro)
            DBSession.flush()

        fases=Fase.get_fase_by_proyecto(id_proyecto)
        for fase in fases:
            Fase.borrar_by_id(fase.id_fase)
            DBSession.flush()

        Proyecto.borrar_by_id(id_proyecto)
        DBSession.flush()

        flash("Proyecto eliminado!")
        redirect('/proyecto/proyecto')

################################################################################

    @expose()
    def salir_proyecto(self):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")
        condicion=int (Variables.get_valor_by_nombre("rol_anterior"))

        if condicion > 0:
            usuario=Usuario.get_user_by_alias(request.identity['repoze.who.userid'])

            Variables.set_valor_by_nombre("fase_actual",0)
            Variables.set_valor_by_nombre("proyecto_actual",0)
            Variables.set_valor_by_nombre("nombre_proyecto_actual","")
            Variables.set_valor_by_nombre("nombre_fase_actual","")
            Variables.set_valor_by_nombre("usuario_actual","")
            rol=int (Variables.get_valor_by_nombre("rol_anterior") )
            Variables.set_valor_by_nombre("rol_actual",rol)
            Variables.set_valor_by_nombre("rol_anterior",0)
            rol2=Rol.get_rol_by_id(rol)
            usuario.roles=[]
            usuario.roles.append(rol2)
            DBSession.flush()

        redirect('/index')

################################################################################

    @expose('saip2011.templates.fase.seleccionar_tipo')
    def seleccionar_tipo(self,id_fase,*args, **kw):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        if id_fase is not None:
            id_fase=int(id_fase)

        fase = DBSession.query(Fase).get(id_fase)
        tipos_items = DBSession.query(Tipo_Item).all()
        
        tipos = fase.tipos_items
        tipos_items2 = []
        for tip in tipos:
            tipos_items2.append(tip.id_tipo_item)

        if request.method != 'PUT':  
            values = dict(id_fase=fase.id_fase, 
                            nombre_fase=fase.nombre_fase, 
                            id_tipo_fase=fase.id_tipo_fase,
                            nombre_tipo_fase=fase.nombre_tipo_fase,
                            estado=fase.estado,
                            linea_base=fase.linea_base,
                            descripcion=fase.descripcion,
                            )

        return dict(pagina="seleccionar_tipo",values=values,
                        tipos_items=tipos_items,tipos_items2=tipos_items2,
                         nom_proyecto=nom_proyecto,nom_fase=nom_fase)

    @validate({'id_fase':Int(not_empty=True), 
                'nombre_fase':NotEmpty, 
                'id_tipo_fase':Int(not_empty=True), 
                }, error_handler=seleccionar_tipo)	

    @expose()
    def put_seleccionar_tipo(self, id_fase, nombre_fase, id_tipo_fase, tipos_items,
                    descripcion, asmSelect0, nombre_tipo_fase,**kw):

        if id_fase is not None:
            id_fase=int(id_fase)

        if id_tipo_fase is not None:
            id_tipo_fase=int(id_tipo_fase)

        fase = Fase.get_fase_by_id(id_fase)

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
        flash("Tipos Item agregados!")
        redirect('/proyecto/proyecto')

################################################################################

