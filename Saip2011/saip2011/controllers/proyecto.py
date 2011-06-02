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
from saip2011.form import UsuarioForm , RolForm , PrivilegioForm , FaseForm , TipoFaseForm 
from saip2011.form import ItemForm , TipoItemForm , EquipoForm , ProyectoForm , TipoCamposForm
from formencode import Invalid
from psycopg2 import IntegrityError



class ProyectoController(BaseController):
    

 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

	@expose('saip2011.templates.proyecto.proyecto')
	def proyecto(self):
		"""
		Menu para Proyecto
		"""
		return dict(pagina="proyecto")
    
	@expose('saip2011.templates.proyecto.listar_proyecto')
	def listar_proyecto(self):
		"""Lista proyectos 
		"""
		proyectos = Proyecto.get_proyecto()
		return dict(pagina="listar_proyecto",proyectos=proyectos)

	@expose('saip2011.templates.proyecto.ingresar_proyecto')
	def ingresar_proyecto(self):
		"""lista de los  proyectos del usuario
		"""
		usuario=Usuario.get_user_by_alias(request.identity['repoze.who.userid'])
		proy = Proyecto.get_proyecto()
		proyectos = []
		miembros=Equipo_Desarrollo.get_miembros_by_usuario(usuario.idusuario)

		for miembro in miembros:
			for p in proy:
				if (miembro.proyecto == p.id_proyecto):
					proyectos.append(p)

		return dict(pagina="ingresar_proyecto",proyectos=proyectos)

	@expose()
	def ingresar(self,id_proyecto):
		usuario=Variables.get_valor_by_nombre("usuario_actual")
		proyecto=Proyecto.get_proyecto_by_id(id_proyecto)
		Variables.set_valor_by_nombre("proyecto_actual",proyecto.id_proyecto)
		miembros=Equipo_Desarrollo.get_miembros_by_proyecto(proyecto.id_proyecto)
		for miembro in miembros:
			if ( miembro.idusuario == usuario.idusuario ):
				Variables.set_valor_by_nombre("rol_actual",miembro.idrol)

		redirect('/proyecto/proyecto')

	@expose('saip2011.templates.proyecto.agregar_proyecto')
	def agregar_proyecto(self, *args, **kw):
		usuarios = DBSession.query(Usuario).all()
		tipos_fases = DBSession.query(Tipo_Fase).all()	

		return dict(pagina="agregar_proyecto",values=kw, tipos_fases=tipos_fases, usuarios=usuarios)
    
	@validate({'nombre_proyecto':NotEmpty, 
				'idusuario':Int(not_empty=True), 
				'tipos_fases':NotEmpty,
				#		'descripcion':NotEmpty
				}, error_handler=agregar_proyecto)

	@expose()
	def post_proyecto(self, nombre_proyecto, idusuario, tipos_fases, asmSelect0, descripcion):
		if idusuario is not None:
			idusuario = int(idusuario)

		if tipos_fases is not None:
			if not isinstance(tipos_fases, list):
				tipos_fases = [tipos_fases]
		tipos_fases = [DBSession.query(Tipo_Fase).get(tipo_fase) for tipo_fase in tipos_fases]
        
		proyecto = Proyecto (nombre_proyecto=nombre_proyecto, idusuario=idusuario, 
				     descripcion=descripcion, tipos_fases=tipos_fases)
		DBSession.add(proyecto)
        
		equipo = Equipo_Desarrollo(proyecto=Variables.get_valor_by_nombre("proyecto_actual"), idusuario=idusuario, 
									idrol=Variables.get_valor_by_nombre("rol_actual"))
		DBSession.add(equipo)
		flash("Proyecto Agregado!")  
		redirect('/proyecto/proyecto')

	@expose('saip2011.templates.proyecto.editar_proyecto')
	def editar_proyecto(self, id_proyecto, *args, **kw):
		usuarios = DBSession.query(Usuario).all()
		tipos_fases = DBSession.query(Tipo_Fase).all()
		proyecto = DBSession.query(Proyecto).get(id_proyecto)
		usuario2 = proyecto.idusuario
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
		return dict(pagina="editar_proyecto",values=values, usuarios=usuarios, tipos_fases=tipos_fases, tipos_fases2=tipos_fases2,usuario2=usuario2)

	@validate({'id_proyecto':Int(not_empty=True), 
				'nombre_proyecto':NotEmpty, 
				'tipos_fases':NotEmpty,
				#               'descripcion':NotEmpty, 
				'idusuario':Int(not_empty=True)}, error_handler=editar_proyecto)

	@expose()
	def put_proyecto(self, id_proyecto, nombre_proyecto, idusuario, descripcion, asmSelect0, tipos_fases,**kw):
		proyecto = DBSession.query(Proyecto).get(id_proyecto)
		miembro=Equipo_Desarrollo.get_miembro(proyecto.idusuario)
		id_miembro=miembro.id_equipo
		DBSession.delete(DBSession.query(Equipo_Desarrollo).get(id_miembro))
		DBSession.flush()
		idusuario = int(idusuario)
		if not isinstance(tipos_fases, list):
			tipos_fases = [tipos_fases]
		tipos_fases = [DBSession.query(Tipo_Fase).get(tipo_fase) for tipo_fase in tipos_fases]
            
		proyecto.idusuario = idusuario
		proyecto.nombre_proyecto=nombre_proyecto
		proyecto.descripcion = descripcion
		proyecto.tipos_fases = tipos_fases
     
		DBSession.flush()
		equipo = Equipo_Desarrollo(proyecto=Variables.get_valor_by_nombre("proyecto_actual"), idusuario=idusuario, 
									idrol=Variables.get_valor_by_nombre("rol_actual"))
		DBSession.add(equipo)

		flash("Proyecto Modificado!")  
		redirect('/proyecto/proyecto')
 
	@expose('saip2011.templates.proyecto.eliminar_proyecto')
	def eliminar_proyecto(self,id_proyecto, *args, **kw):
		proyecto = DBSession.query(Proyecto).get(id_proyecto)	

		values = dict(id_proyecto=proyecto.id_proyecto, 
						nombre_proyecto=proyecto.nombre_proyecto, 
						descripcion=proyecto.descripcion,
						lider_equipo=proyecto.lider_equipo,
						tipos_fases=proyecto.tipos_fases
						)

		return dict(pagina="eliminar_proyecto",values=values)

	@validate({'id_proyecto':Int(not_empty=True), 
				'nombre_proyecto':NotEmpty, 
				'tipos_fases':NotEmpty,
				#               'descripcion':NotEmpty
				}, error_handler=eliminar_proyecto)	

	@expose()
	def post_delete_proyecto(self, id_proyecto, nombre_proyecto, descripcion, tipos_fases, **kw):

		proyecto = DBSession.query(Proyecto).get(id_proyecto)
		miembros=Equipo_Desarrollo.get_miembros_by_proyecto(proyecto.idusuario)
		for miembro in miembros:
			idm=miembro.id_equipo
			DBSession.delete(DBSession.query(Equipo_Desarrollo).get(idm))
			#DBSession.flush()

		DBSession.delete(DBSession.query(Proyecto).get(id_proyecto))
		DBSession.flush()
		flash("Proyecto eliminado!")
		redirect('/proyecto/proyecto')

