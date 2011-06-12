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
from saip2011.form import  TipoFaseForm , TipoCamposForm
from formencode import Invalid
from psycopg2 import IntegrityError



class EquipoController(BaseController):
    

################################################################################ 

    @expose('saip2011.templates.miembro.listar_miembro')
    def equipo(self):
        """
        Menu para Equipo de Desarrollo
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")
        valor=int( Variables.get_valor_by_nombre("proyecto_actual"))
        equipos =  Equipo_Desarrollo.get_miembros_by_proyecto(valor)
        return dict(pagina="listar_miembro",equipos=equipos,
                        nom_proyecto=nom_proyecto,nom_fase=nom_fase)
        #return dict(pagina="equipo",nom_proyecto=nom_proyecto)

################################################################################
    
    @expose('saip2011.templates.miembro.listar_miembro')
    def listar_miembro(self):
        """Lista equipos 
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")
        valor=int( Variables.get_valor_by_nombre("proyecto_actual"))
        equipos =  Equipo_Desarrollo.get_miembros_by_proyecto(valor)
        return dict(pagina="listar_miembro",equipos=equipos,
                        nom_proyecto=nom_proyecto,nom_fase=nom_fase)

################################################################################

    @expose('saip2011.templates.miembro.listar_mis_fases')
    def ver_fases(self,id_equipo):
        """Lista  
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")
        miembro=Equipo_Desarrollo.get_miembro_by_id(int(id_equipo))
        values = dict(id_equipo=miembro.id_equipo, 
		                nombre_usuario=miembro.nombre_usuario, 
		                nombre_rol=miembro.nombre_rol
		                )

        fas = miembro.fases
        fases = []
        for f in fas:
            fases.append(f)
        return dict(pagina="listar_mis_fases",fases=fases,
                        nom_proyecto=nom_proyecto,nom_fase=nom_fase,
                        values=values)

###############################################################################

    @expose('saip2011.templates.miembro.agregar_miembro')
    def agregar_miembro(self, *args, **kw):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")
        proy=int(Variables.get_valor_by_nombre("proyecto_actual") )
        roles = DBSession.query(Rol).all()
        usuarios = DBSession.query(Usuario).all()
        miembros=Equipo_Desarrollo.get_miembros_by_proyecto(proy)
        fases = Fase.get_fase_by_proyecto(proy)
        lider=Rol.get_rol_by_nombre("Lider Proyecto")

        if usuarios is not None:
            if not isinstance(usuarios, list):
                usuarios = [usuarios]
        if roles is not None:
            if not isinstance(roles, list):
                roles = [roles]
        if miembros is not None:
            if not isinstance(miembros, list):
                miembros = [miembros]

        for usuario in usuarios:
            for miembro in miembros:
                if usuario.idusuario == miembro.idusuario:
                    usuarios.remove(usuario)

        for miembro in miembros:
            for rol in roles:
                if rol.idrol == miembro.idrol:          
                    roles.remove(rol)
                if rol.nombrerol =="Administrador":
                    roles.remove(rol)            


        return dict(pagina="agregar_miembro",values=kw, roles=roles,
                     usuarios=usuarios, fases=fases,nom_proyecto=nom_proyecto
                     ,nom_fase=nom_fase)
    
    @validate({'idusuario':Int(not_empty=True),
				'fases':NotEmpty,
				'idrol':Int(not_empty=True)}, error_handler=agregar_miembro)

    @expose()
    def post_miembro(self, idusuario, idrol, asmSelect0, fases):
        if idusuario is not None:
            idusuario = int(idusuario)      
        if idrol is not None:
            idrol = int(idrol)      

        if fases is not None:
            if not isinstance(fases, list):
                fases = [fases]
        fases = [DBSession.query(Fase).get(fase) for fase in fases]

        valor=int( Variables.get_valor_by_nombre("proyecto_actual"))
        equipo =  Equipo_Desarrollo(proyecto=valor, idusuario=idusuario, 
							        idrol=idrol, fases=fases)

        usuario = DBSession.query(Usuario).get(idusuario)
        rol = DBSession.query(Rol).get(idrol)
        usuario.roles=[]
        usuario.roles.append(rol)
        DBSession.add(equipo)
        DBSession.flush()

        flash("Miembro Agregado Agregado!")  
        redirect('/equipo/equipo')

################################################################################

    @expose('saip2011.templates.miembro.editar_miembro')
    def editar_miembro(self, id_equipo, *args, **kw):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")      
        usuarios = DBSession.query(Usuario).all()
        roles = DBSession.query(Rol).all()
        equipo = DBSession.query(Equipo_Desarrollo).get(id_equipo)
        proy=int(Variables.get_valor_by_nombre("proyecto_actual") )
        fases = Fase.get_fase_by_proyecto(proy)

        fasess = equipo.fases
        fases2 = []
        for fas in fasess:
            fases2.append(fas.id_fase)

        usuario2=equipo.nombre_usuario
        rol2=equipo.nombre_rol
        values = dict(id_equipo=equipo.id_equipo, 
				  nombre_usuario=equipo.nombre_usuario, 
				  nombre_rol=equipo.nombre_rol
		                  )
		                  
        values.update(kw)

        return dict(values=values, usuarios=usuarios, roles=roles , 
                        usuario2=usuario2, rol2=rol2,fases2=fases2, fases=fases,
                        nom_proyecto=nom_proyecto,nom_fase=nom_fase)

    @validate({'idusuario':Int(not_empty=True),
				'fases':NotEmpty,
				'idrol':Int(not_empty=True)}, error_handler=editar_miembro)

    @expose()
    def put_miembro(self, id_equipo, idusuario, idrol, asmSelect0, fases,
                     **kw):

        equipo = DBSession.query(Equipo_Desarrollo).get(id_equipo)

        if idusuario is not None:
            idusuario = int(idusuario)      
        if idrol is not None:
            idrol = int(idrol)   
        if not isinstance(fases, list):
            fases = [fases]
        fases = [DBSession.query(Fase).get(fase) for fase in fases]
           
        equipo.idusuario = idusuario
        equipo.idrol=idrol
        equipo.fases

        DBSession.flush()
        flash("Miembro Modificado!")  
        redirect('/equipo/equipo')

################################################################################
 
    @expose('saip2011.templates.miembro.eliminar_miembro')
    def eliminar_miembro(self,id_equipo, *args, **kw):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")
        equipo = DBSession.query(Equipo_Desarrollo).get(id_equipo)	

        values = dict(id_equipo=equipo.id_equipo, 
		      nombre_usuario=equipo.nombre_usuario, 
		      nombre_rol=equipo.nombre_rol
                      )

        return dict(pagina="eliminar_miembro",values=values,
                        nom_proyecto=nom_proyecto,nom_fase=nom_fase)

    @validate({'nombre_usuario':NotEmpty,
		'nombre_rol':NotEmpty}, error_handler=eliminar_miembro)

    @expose()
    def post_delete_miembro(self, id_equipo, nombre_usuario, nombre_rol, **kw):
        DBSession.delete(DBSession.query(Equipo_Desarrollo).get(id_equipo))
        DBSession.flush()	
        flash("Miembro eliminado!")
        redirect('/equipo/equipo')

