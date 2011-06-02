# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, request, redirect
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from catwalk.tg2 import Catwalk
from repoze.what import predicates
from tgext.crud import CrudRestController
from sprox.tablebase import TableBase
from sprox.fillerbase import TableFiller

from saip2011.lib.base import BaseController
from saip2011.model import DBSession, metadata
from saip2011.controllers.error import ErrorController
from saip2011 import model
from saip2011.model.auth import Usuario
from saip2011.controllers.secure import SecureController
from cherrypy import HTTPRedirect
from genshi.template import TemplateLoader
import os
from saip2011.form import UsuarioForm
from formencode import Invalid
import transaction
from psycopg2 import IntegrityError


loader = TemplateLoader(
    os.path.join(os.path.dirname(__file__),'templates'),
    auto_reload=True)

"""__all__ = ['RootController','UsuarioController']
usuario = "desconocido"""

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
    secc = SecureController()
    
    admin = Catwalk(model, DBSession)
    proyecto = Catwalk(model,DBSession)
    
    error = ErrorController()

    

    @expose('saip2011.templates.index')
    def index(self):
        """Pagina de inicio, si no esta autenticado todavia!
           redirije a la pagina de login   
        """
	if not request.identity:
        
             redirect(url('/login', came_from=url('/')))
       
        return dict(pagina='index')

    @expose('saip2011.templates.about')
    def nosotros(self):
        """Maneja la pagina nosotros"""
        return dict(pagina='about')
 
    @expose('saip2011.templates.contact')
    def contactos(self):
        """Maneja la pagina contactos"""
        return dict(pagina='contact')

    @expose('saip2011.templates.authentication')
    def autenticacion(self):
        """Display some information about auth* on this application."""
        return dict(pagina='auth')

    @expose('saip2011.templates.index')
    @require(predicates.has_permission('control_total', msg=l_('Solo para administradores')))
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
        usuario = userid
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
    
    @expose('saip2011.templates.usuario')
    def usuario(self):
        """
           Menu para USUARIO
        """
        return dict(pagina="usuario")
    
    @expose('saip2011.templates.editar_usuario')
    def user(self,iduser,action):
        """
           Metodo que recibe ID de usuario para
           ser modificado
        """
        return "Pagina no disponible"
    
    @expose('saip2011.templates.listar_usuario')
    def listar_usuario(self):
        """Lista usuarios 
        """
        usuarios = Usuario.get_usuarios()
        return dict(pagina="listar_usuario",usuarios=usuarios)

    @expose('saip2011.templates.agregar_usuario')
    def agregar_usuario(self,cancel=False,**data):
        errors = {}
        usuario = None
        if request.method == 'POST':
            if cancel:
                redirect('/usuario')
            form = UsuarioForm()
            try:
                data = form.to_python(data)
                usuario = Usuario(alias=data.get('alias'),nombre=data.get('nombre'),apellido=data.get('apellido'),email_address=data.get('email'))
                #if isinstance(usuario,Usuario) :
                DBSession.add(usuario)
                DBSession.flush()
                DBSession.commit()
                transaction.commit() 
                print usuario
                flash("Usuario agregado!")
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
        #aqui se debe guardar los datos obtenidos
        #usuario = Usuario(data[0])
        #tmpl = loader.load('agregar_usuario.html')
        #stream = tmpl.generate()
        #return stream.render('html',doctype='html')
        return dict(pagina='agregar_usuario',data=data.get('alias'),errors=errors)


    

