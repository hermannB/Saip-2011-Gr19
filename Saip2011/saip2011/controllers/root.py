# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, request, redirect
from datetime import datetime
from tg.controllers import RestController, redirect
from tg.decorators import expose, validate
from formencode.validators import DateConverter, Int, NotEmpty

from pylons.i18n import ugettext as _, lazy_ugettext as l_
from catwalk.tg2 import Catwalk
from repoze.what import predicates
from tgext.crud import CrudRestController
#from sprox.tablebase import TableBase
#from sprox.fillerbase import TableFiller
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
from saip2011.model.variables import Variables
from saip2011.controllers.secure import SecureController
from cherrypy import HTTPRedirect
from genshi.template import TemplateLoader
import os
from saip2011.form import UsuarioForm , RolForm , PrivilegioForm , FaseForm
from saip2011.form import ItemForm , TipoItemForm , EquipoForm , ProyectoForm 
from saip2011.form import TipoFaseForm , TipoCamposForm
from formencode import Invalid
from psycopg2 import IntegrityError
from saip2011.controllers.fase import FaseController
from saip2011.controllers.equipo import EquipoController
from saip2011.controllers.item import ItemController
from saip2011.controllers.proyecto import ProyectoController
from saip2011.controllers.tipo_fase import Tipo_FaseController
from saip2011.controllers.tipo_item import Tipo_ItemController
#from saip2011.controllers.reporte import ReporteController

__all__ = ['RootController', 'FaseController' , 'EquipoController' ,
         'ItemController' , 'ProyectoController' ,  'Tipo_FaseController' 
            , 'Tipo_ItemController' ]


	

class RootController(BaseController):
    """
    The root controller for the saip2011 application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

	    panel = ControlPanelController()
	    another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """

    fase = FaseController()
    equipo = EquipoController()
    item = ItemController()
    proyecto = ProyectoController()
    #    reporte = ReporteController()
    tipo_fase = Tipo_FaseController()
    tipo_item = Tipo_ItemController()

    secc = SecureController()

    #    admin = Catwalk(model, DBSession)
    #    proyecto = Catwalk(model,DBSession)

    error = ErrorController()


################################################################################

    @expose('saip2011.templates.index')
    def index(self):
        """Pagina de inicio, si no esta autenticado todavia!
        redirije a la pagina de login   
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        if not request.identity:
            redirect(url('/login', came_from=url('/')))
        return dict(pagina='index',nom_proyecto=nom_proyecto)

    @expose('saip2011.templates.about')
    def nosotros(self):
        """Maneja la pagina nosotros"""
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        return dict(pagina='about',nom_proyecto=nom_proyecto)
 
    @expose('saip2011.templates.contact')
    def contactos(self):
        """Maneja la pagina contactos"""
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        return dict(pagina='contact',nom_proyecto=nom_proyecto)

    @expose('saip2011.templates.authentication')
    def autenticacion(self):
        """Display some information about auth* on this application."""
        return dict(pagina='auth')

    @expose('saip2011.templates.index')
    @require(predicates.has_permission('control_total', 
                msg=l_('Solo para administradores')))
    def solo_permiso_solo(self, **kw):
        """Illustrate how a page for managers only works."""
        return dict(pagina='managers stuff')

    @expose('saip2011.templates.index')
    @require(predicates.is_user('editor', msg=l_('Only for the editor')))
    def editor_user_only(self, **kw):
        """Illustrate how a page exclusive for the editor works."""
        return dict(pagina='editor stuff')

    @expose('saip2011.templates.login')
    def login(self, came_from=url('/')):
        """Start the user login."""
        login_counter = request.environ['repoze.who.logins']
        if login_counter > 0:
            flash(_('datos incorrectos..'), 'warning')
        return dict(pagina='login', login_counter=str(login_counter),
					came_from=came_from)
    
    @expose()
    def post_login(self, came_from=url('/')):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ['repoze.who.logins'] + 1
            redirect(url('/login', came_from=came_from, __logins=login_counter))
        userid = request.identity['repoze.who.userid']
        Variables.set_valor_by_nombre("usuario_actual",userid)

        flash(_('Bienvenido, %s!') % userid)
        redirect(came_from)

    @expose()
    def post_logout(self, came_from=url('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('Hasta luego!') )
        redirect('/')

 ################################################################################
    
    @expose('saip2011.templates.usuario.usuario')
    def usuario(self):
        """
        Menu para USUARIO
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        return dict(pagina="usuario",nom_proyecto=nom_proyecto)

 ################################################################################

    @expose('saip2011.templates.usuario.cambiar_password')
    def cambiar_password(self):
        """
           Metodo que prepara los campos para 
           modificar el pass
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        return dict(pagina="cambiar_password",nom_proyecto=nom_proyecto)

    @expose()
    def post_cambiar_password(self,clave,clave2,cancel=False):
        """
        Metodo que usa el Id del usuario logeado
        para modificar su password
        """
        if cancel:
            redirect('/usuario')

        var=Variables.get_valor_by_nombre("usuario_actual")
        usuario = Usuario.get_user_by_alias(var)
        usuario._set_password(clave)
        flash("password modificado!")
        redirect('/usuario')

 ################################################################################
    
    @expose('saip2011.templates.usuario.editar_usuario')
    def editar_usuario(self,idusuario,cancel=False,*args, **kw):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        usuario = DBSession.query(Usuario).get(idusuario)

        if cancel:
            redirect('/usuario')

        if request.method != 'PUT':  

            values = dict(idusuario=usuario.idusuario, 
					alias=usuario.alias, 
					nombre=usuario.nombre, 
					apellido=usuario.apellido,
					nacionalidad=usuario.nacionalidad,
					tipodocumento=usuario.tipodocumento,
					nrodoc=usuario.nrodoc,
					email_address=usuario.email_address,
					)
        return dict(pagina="editar_usuario",values=values,
                        nom_proyecto=nom_proyecto)

    @validate({'idusuario':NotEmpty, 
				'alias':NotEmpty, 
				'nombre':NotEmpty, 
				'apellido':NotEmpty, 
				'nrodoc':Int(not_empty=True),
				'email_address':NotEmpty}, error_handler=editar_usuario)	
  
    @expose()
    def put_usuario(self, idusuario, alias, nombre,  apellido, nacionalidad,
                         tipodocumento, nrodoc , email_address,cancel=False, 
                            **kw):

        if cancel:
            redirect('/usuario')

        usuario = DBSession.query(Usuario).get(int(idusuario))

        usuario.alias=alias, 
        usuario.nombre=nombre, 
        usuario.apellido=apellido,
        usuario.nacionalidad=nacionalidad,
        usuario.tipodocumento=tipodocumento,
        usuario.nrodoc=nrodoc,
        usuario.email_address=email_address,

        DBSession.flush()
        flash("Usuario modificado!")
        redirect('/usuario')

 ################################################################################

    @expose('saip2011.templates.usuario.listar_usuario')
    def listar_usuario(self):
        """Lista usuarios 
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        usuarios = Usuario.get_usuarios()
        return dict(pagina="listar_usuario",usuarios=usuarios,
                        nom_proyecto=nom_proyecto)

 ################################################################################

    @expose('saip2011.templates.usuario.eliminar_usuario')
    def eliminar_usuario(self,idusuario, *args, **kw):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")	
        usuario = DBSession.query(Usuario).get(idusuario)	

        values = dict(idusuario=usuario.idusuario, 
						alias=usuario.alias, 
						nombre=usuario.nombre, 
						apellido=usuario.apellido,
						nacionalidad=usuario.nacionalidad,
						tipodocumento=usuario.tipodocumento,
						nrodoc=usuario.nrodoc,
						email_address=usuario.email_address
						)

        return dict(pagina="eliminar_usuario",values=values,
                        nom_proyecto=nom_proyecto)

    @validate({'idusuario':NotEmpty, 
				'alias':NotEmpty, 
				'nombre':NotEmpty, 
				'apellido':NotEmpty, 
				'nrodoc':Int(not_empty=True),
				'email_address':NotEmpty}, error_handler=eliminar_usuario)	
    
    @expose()
    def post_delete_usuario(self, idusuario, alias, nombre, apellido, 
                                nacionalidad, tipodocumento, nrodoc , 
                                email_address ,  **kw):
	
        DBSession.delete(DBSession.query(Usuario).get(idusuario))
        DBSession.flush()
        flash("Usuario eliminado!")
        redirect('/usuario')

 ################################################################################

    @expose('saip2011.templates.usuario.agregar_usuario')
    def agregar_usuario(self,cancel=False,**data):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        errors = {}
        usuario = None
        if request.method == 'POST':
            if cancel:
                redirect('/usuario')
            form = UsuarioForm()
            try:
                data = form.to_python(data)

                usuario = Usuario(alias=data.get('alias'),
                                    nombre=data.get('nombre'),
                                    apellido=data.get('apellido'),
                                    email_address=data.get('email'),
                                    nacionalidad=data.get('nacionalidad'),
									tipodocumento=data.get('tipodocumento'),
                                    nrodoc=data.get('nrodoc'),
									_password=data.get('clave'))

                usuario._set_password(data.get('clave'))
                xdef=int (Variables.get_valor_by_nombre("rol_por_defecto") )
                rol = DBSession.query(Rol).get(xdef)
                usuario.roles.append(rol)
                DBSession.add(usuario)
                DBSession.flush()
                print usuario
                flash("Usuario agregado!")
                redirect('/usuario')
            except Invalid, e:
                print e
                usuario = None
                errors = e.unpack_errors()
                flash(_("Favor complete los datos requeridos"),'warning')
            except IntegrityError:
                flash("LLave duplicada")
                DBSession.rollback()
                redirect('/agregar_usuario')
        else:
            errors = {}        
            return dict(pagina='usuarios',data=data.get('alias'),errors=errors,
                                nom_proyecto=nom_proyecto)

 ################################################################################
 ################################################################################

    @expose('saip2011.templates.rol.listar_rol')
    def rol(self):
        """
        Menu para Rol
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        roles = Rol.get_roles()
        return dict(pagina="listar_rol",roles=roles,nom_proyecto=nom_proyecto)
        #return dict(pagina="rol",nom_proyecto=nom_proyecto)

 ################################################################################
    
    @expose('saip2011.templates.rol.editar_rol')
    def editar_rol(self, idrol, *args, **kw):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        privilegios = DBSession.query(Privilegios).all()
        rol = DBSession.query(Rol).get(idrol)
        priv = rol.privilegios
        privilegios2 = []
        for p in priv:
            privilegios2.append(p.idprivilegio)
        
        values = dict(idrol=rol.idrol, 
						nombrerol=rol.nombrerol, 
						descripcion=rol.descripcion
						)
                      
        if 'privilegios' in kw and not isinstance(kw['privilegios'], list):
            kw['privilegios'] = [kw['privilegios']]

        values.update(kw)
        return dict(pagina="editar_rol",values=values,  privilegios=privilegios ,
                         privilegios2=privilegios2,nom_proyecto=nom_proyecto)

    @validate({'idrol':Int(not_empty=True), 
				'nombrerol':NotEmpty, 
				#       'descripcion':NotEmpty
				}, error_handler=editar_rol)

    @expose()
    def put_rol(self, idrol, nombrerol, descripcion, privilegios, **kw):
        rol = DBSession.query(Rol).get(idrol)
        if not isinstance(privilegios, list):
            privilegios = [privilegios]
        privilegios = [DBSession.query(Privilegios).get(privilegio) for privilegio
                         in privilegios]
        rol.nombrerol=nombrerol
        rol.descripcion = descripcion
        rol.privilegios = privilegios

        DBSession.flush()
        flash("Rol modificado!")
        redirect('/rol')

 ################################################################################   

    @expose('saip2011.templates.rol.listar_rol')
    def listar_rol(self):
        """Lista Roles 
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        roles = Rol.get_roles()
        return dict(pagina="listar_rol",roles=roles,nom_proyecto=nom_proyecto)

 ################################################################################

    @expose('saip2011.templates.rol.eliminar_rol')
    def eliminar_rol(self,idrol, *args, **kw):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        rol = DBSession.query(Rol).get(idrol)	
        values = dict(idrol=rol.idrol, 
						nombrerol=rol.nombrerol, 
						descripcion=rol.descripcion,
						privilegios=rol.privilegios
						)

        return dict(pagina="eliminar_rol",values=values,
                        nom_proyecto=nom_proyecto)

    @validate({'idrol':NotEmpty, 
				'nombrerol':NotEmpty, 
				#         'descripcion':NotEmpty
				}, error_handler=eliminar_rol)	

    @expose()
    def post_delete_rol(self, idrol, nombrerol, descripcion, privilegios, **kw):
        DBSession.delete(DBSession.query(Rol).get(idrol))
        DBSession.flush()
        flash("Rol eliminado!")
        redirect('/rol')

    @expose('saip2011.templates.rol.agregar_rol')
    def agregar_rol(self, *args, **kw):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        privilegios = DBSession.query(Privilegios).all()

        return dict(pagina="agregar_rol",values=kw, privilegios=privilegios,
                        nom_proyecto=nom_proyecto)

    @validate({'nombrerol':NotEmpty, 
			#'descripcion':NotEmpty
			},error_handler=agregar_rol)

    @expose()
    def post_rol(self, nombrerol, descripcion, privilegios=None):
        if privilegios is not None:
            if not isinstance(privilegios, list):
                privilegios = [privilegios]
        privilegios = [DBSession.query(Privilegios).get(privilegio) 
                        for privilegio in privilegios]
        rol = Rol(nombrerol=nombrerol, descripcion=descripcion,
                    privilegios=privilegios)

        DBSession.add(rol)
        DBSession.flush()
        flash("Rol agregado!")
        redirect('/rol')

 ################################################################################
 ################################################################################

    @expose('saip2011.templates.privilegio.listar_privilegio')
    def privilegio(self):
        """
        Menu para Privilegio
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        privilegios = Privilegios.get_privilegio()
        return dict(pagina="listar_privilegio",privilegios=privilegios,
                        nom_proyecto=nom_proyecto)
        #return dict(pagina="privilegenres = DBSession.query(Genre).all()gio",
         #               nom_proyecto=nom_proyecto)

 ################################################################################
    
    @expose('saip2011.templates.privilegio.editar_privilegio')
    def editar_privilegio(self,idprivilegio,*args, **kw):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        privilegio = DBSession.query(Privilegios).get(idprivilegio)
        if request.method != 'PUT':  
            values = dict(idprivilegio=privilegio.idprivilegio, 
					        nombreprivilegio=privilegio.nombreprivilegio, 
					        descripcion=privilegio.descripcion,
					        )

        return dict(pagina="editar_privilegio",values=values,
                nom_proyecto=nom_proyecto)

    @validate({'idprivilegio':Int(not_empty=True), 
				'nombreprivilegio':NotEmpty, 
				'descripcion':NotEmpty}, error_handler=editar_privilegio)	

    @expose()
    def put_privilegio(self, idprivilegio, nombreprivilegio, descripcion, **kw):
        privilegio = DBSession.query(Privilegios).get(int(idprivilegio))
        privilegio.nombreprivilegio = nombreprivilegio
        privilegio.descripcion = descripcion
        DBSession.flush()
        flash("Privilegio modificado!")
        redirect('/privilegio') 

################################################################################

    @expose('saip2011.templates.privilegio.listar_privilegio')
    def listar_privilegio(self):
        """Lista privilegios 
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        privilegios = Privilegios.get_privilegio()
        return dict(pagina="listar_privilegio",privilegios=privilegios,
                        nom_proyecto=nom_proyecto)

 ################################################################################

    @expose('saip2011.templates.privilegio.eliminar_privilegio')
    def eliminar_privilegio(self,idprivilegio, *args, **kw):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        privilegio = DBSession.query(Privilegios).get(idprivilegio)	
        values = dict(idprivilegio=privilegio.idprivilegio, 
					nombreprivilegio=privilegio.nombreprivilegio, 
					descripcion=privilegio.descripcion,
					)

        return dict(pagina="eliminar_privilegio",values=values,
                        nom_proyecto=nom_proyecto)

    @validate({'idprivilegio':Int(not_empty=True), 
				'nombreprivilegio':NotEmpty, 
				#       'descripcion':NotEmpty
				}, error_handler=eliminar_privilegio)	

    @expose()
    def post_delete_privilegio(self, idprivilegio, nombreprivilegio, descripcion,
                                    **kw):
        DBSession.delete(DBSession.query(Privilegios).get(idprivilegio))
        DBSession.flush()
        flash("Privilegio eliminado!")
        redirect('/privilegio')

 ################################################################################

    @expose('saip2011.templates.privilegio.agregar_privilegio')
    def agregar_privilegio(self,cancel=False,**data):
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        errors = {}
        privilegio = None
        if request.method == 'POST':
            if cancel:
                redirect('/privilegio')
            form = PrivilegioForm()
            try:
                data = form.to_python(data)
                privilegio = Privilegios(
                                nombreprivilegio=data.get('nombreprivilegio'),
								descripcion=data.get('descripcion'))

                DBSession.add(privilegio)
                DBSession.flush()
                print privilegio
                flash("Privilegio agregado!")
            except Invalid, e:
                print e
                privilegio = None
                errors = e.unpack_errors()
                flash(_("Favor complete los datos requeridos"),'warning')
            except IntegrityError:
                flash("LLave duplicada")
                DBSession.rollback()
                redirect('/agregar_privilegio')
        else:
            errors = {}        
            return dict(pagina='agregar_privilegio',
                            data=data.get('nombreprivilegio'),errors=errors,
                            nom_proyecto=nom_proyecto)

 ################################################################################


