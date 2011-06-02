# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, request, redirect

from tg.controllers import RestController, redirect
from tg.decorators import expose, validate
from formencode.validators import DateConverter, Int, NotEmpty

from pylons.i18n import ugettext as _, lazy_ugettext as l_
from catwalk.tg2 import Catwalk
from repoze.what import predicates
from tgext.crud import CrudRestController
from sprox.tablebase import TableBase
from sprox.fillerbase import TableFiller
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

 
from saip2011.controllers.secure import SecureController
from cherrypy import HTTPRedirect
from genshi.template import TemplateLoader
import os
from saip2011.form import UsuarioForm , RolForm , PrivilegioForm , FaseForm , TipoFaseForm 
from saip2011.form import ItemForm , TipoItemForm , EquipoForm , ProyectoForm
from formencode import Invalid
import transaction
from psycopg2 import IntegrityError


loader = TemplateLoader(
    os.path.join(os.path.dirname(__file__),'templates'),
    auto_reload=True)

"""__all__ = ['RootController','UsuarioController','FaseController']
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
                usuario = Usuario(alias=data.get('alias'),nombre=data.get('nombre'),apellido=data.get('apellido'),email_address=data.get('email'),nacionalidad=data.get('nacionalidad'),tipodocumento=data.get('tipodocumento'),nrodoc=data.get('nrodoc'),_password=data.get('clave'))
                #if isinstance(usuario,Usuario) :
		usuario._set_password(data.get('clave'))
                DBSession.add(usuario)
                DBSession.flush()
                #DBSession.commit()
                #transaction.commit() 
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

 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @expose('saip2011.templates.rol')
    def rol(self):
        """
           Menu para Rol
        """
        return dict(pagina="rol")
    
    @expose('saip2011.templates.editar_rol')
    def rolmod(self,idrol,action):
        """
           Metodo que recibe ID del rol para
           ser modificado
        """
        return "Pagina no disponible"
    
    @expose('saip2011.templates.listar_rol')
    def listar_rol(self):
        """Lista Roles 
        """
        roles = Rol.get_roles()
        return dict(pagina="listar_rol",roles=roles)


    @expose('saip2011.templates.agregar_rol')
    def agregar_rol(self, *args, **kw):
        privilegios = DBSession.query(Privilegios).all()
        
      #  if 'privilegios' in kw and not isinstance(kw['privilegios'], list):
       #     kw['privilegios'] = [kw['privilegios']]

        return dict(pagina="agregar_rol",values=kw, privilegios=privilegios)
    
    @validate({'nombrerol':NotEmpty, 
               'descripcion':NotEmpty}, 
                error_handler=agregar_rol)
   
    @expose()
    def post(self, nombrerol, descripcion, privilegios=None):
        flash("Rol agregado!")
        if privilegios is not None:
            if not isinstance(privilegios, list):
                privilegios = [privilegios]
            privilegios = [DBSession.query(Privilegios).get(privilegio) for privilegio in privilegios]
        rol = Rol(nombrerol=nombrerol, descripcion=descripcion, privilegios=privilegios)
        DBSession.add(rol)
	DBSession.flush()
        redirect('./')
 
#   @expose('saip2011.templates.agregar_rol')
#    def agregar_rol(self,cancel=False,**data):
#        errors = {}
#       	rol = None
#        if request.method == 'POST':
#            if cancel:
#                redirect('/rol')
#            form = RolForm()
#            try:
#                data = form.to_python(data)
#                rol = Rol(nombrerol=data.get('nombrerol'),descripcion=data.get('descripcion'),privilegios=data.get('privilegios'))
#                #if isinstance(usuario,Usuario) :
#                DBSession.add(rol)
#                DBSession.flush()
#                #DBSession.commit()
#                #transaction.commit() 
#                print rol
#                flash("Rol agregado!")
#            except Invalid, e:
#                print e
#                rol = None
#                errors = e.unpack_errors()
#                flash(_("Favor complete los datos requeridos"),'warning')
#            except IntegrityError:
#                flash("LLave duplicada")
#                DBSession.rollback()
#                redirect('/agregar_rol')
#            
#        else:
#            errors = {}        
#        #aqui se debe guardar los datos obtenidos
#        #usuario = Usuario(data[0])
#        #tmpl = loader.load('agregar_usuario.html')
#        #stream = tmpl.generate()
#        #return stream.render('html',doctype='html')
#        return dict(pagina='agregar_rol',data=data.get('nombrerol'),errors=errors)
#

 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @expose('saip2011.templates.privilegio')
    def privilegio(self):
        """
           Menu para Privilegio
        """
        return dict(pagina="privilegio")
    
    @expose('saip2011.templates.editar_privilegio')
    def privilegiomod(self,idprivilegio,action):
        """
           Metodo que recibe ID de privilegio para
           ser modificado
        """
        return "Pagina no disponible"
    
    @expose('saip2011.templates.listar_privilegio')
    def listar_privilegio(self):
        """Lista privilegios 
        """
        privilegios = Privilegios.get_privilegio()
        return dict(pagina="listar_privilegio",privilegios=privilegios)

    @expose('saip2011.templates.agregar_privilegio')
    def agregar_privilegio(self,cancel=False,**data):
        errors = {}
        privilegio = None
        if request.method == 'POST':
            if cancel:
                redirect('/privilegio')
            form = PrivilegioForm()
            try:
                data = form.to_python(data)
                privilegio = Privilegios(nombreprivilegio=data.get('nombreprivilegio'),descripcion=data.get('descripcion'))
                #if isinstance(usuario,Usuario) :
                DBSession.add(privilegio)
                DBSession.flush()
                #DBSession.commit()
                #transaction.commit() 
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
        #aqui se debe guardar los datos obtenidos
        #usuario = Usuario(data[0])
        #tmpl = loader.load('agregar_usuario.html')
        #stream = tmpl.generate()
        #return stream.render('html',doctype='html')
        return dict(pagina='agregar_privilegio',data=data.get('nombreprivilegio'),errors=errors)

 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @expose('saip2011.templates.fase')
    def fase(self):
        """
           Menu para Fases
        """
        return dict(pagina="fase")
        
    @expose('saip2011.templates.listar_fase')
    def listar_fase(self):
        """Lista fases 
        """
        fases = Fase.get_fase()
        return dict(pagina="listar_fase",fases=fases)

    @expose('saip2011.templates.opciones')
    def opciones(self):
        """opciones fases 
        """
        fases = Fase.get_fase()
        return dict(pagina="opciones",fases=fases)
    
    @expose('saip2011.templates.editar_fase')
    def editar_fase(self,id_fase,*args, **kw):
	#id_fase=6
	fase = DBSession.query(Fase).get(id_fase)
	if request.method != 'POST':  
	  #genres = DBSession.query(Genre).all()
          #directors = DBSession.query(Director).all()
          values = dict(id_fase=fase.id_fase, 
	  	        nombre_fase=fase.nombre_fase, 
                        tipo_fase=fase.tipo_fase, 
                        estado=fase.estado,
                        linea_base=fase.linea_base,
                        descripcion=fase.descripcion,
                     # directors = [str(director.director_id) for director in movie.directors],
                     # release_date = datetime.strftime(movie.release_date, "%m/%d/%y"),
                    )
	  return dict(pagina="editar_fase",values=values)


    @validate({'id_fase':NotEmpty, 
	       'nombre_fase':NotEmpty, 
               'tipo_fase':NotEmpty, 
               'estado':NotEmpty, 
               'descripcion':NotEmpty}, error_handler=editar_fase)	
    @expose()
    def put(self, id_fase, nombre_fase, tipo_fase, estado, linea_base, descripcion, **kw):
	
	fase = DBSession.query(Fase).get(int(id_fase))
        
        fase.nombre_fase = nombre_fase
        fase.tipo_fase=tipo_fase
        fase.estado = estado
        fase.linea_base = linea_base
        fase.descripcion = descripcion

        DBSession.flush()
        flash("Fase agregada!")
	redirect('/fase')

    @expose('saip2011.templates.eliminar_fase')
    def eliminar_fase(self,id_fase, *args, **kw):
	
        fase2 = DBSession.query(Fase).get(id_fase)	

	values = dict(id_fase=fase2.id_fase, 
		     nombre_fase=fase2.nombre_fase, 
                     tipo_fase=fase2.tipo_fase, 
                     estado=fase2.estado,
                     linea_base=fase2.linea_base,
                     descripcion=fase2.descripcion,
                     # directors = [str(director.director_id) for director in movie.directors],
                     # release_date = datetime.strftime(movie.release_date, "%m/%d/%y"),
                    )
        return dict(pagina="eliminar_fase",values=values)

    @validate({'id_fase':NotEmpty, 
	       'nombre_fase':NotEmpty, 
               'tipo_fase':NotEmpty, 
               'estado':NotEmpty, 
               'descripcion':NotEmpty}, error_handler=eliminar_fase)	
    @expose()
    def post_delete(self, id_fase, nombre_fase, tipo_fase, estado, linea_base, descripcion, **kw):
	
        DBSession.delete(DBSession.query(Fase).get(id_fase))
        DBSession.flush()
        flash("Fase eliminada!")
	redirect('/fase')

    @expose('saip2011.templates.agregar_fase')
    def agregar_fase(self,cancel=False,**data):
        errors = {}
        fase = None
        if request.method == 'POST':
            if cancel:
                redirect('/fase')
            form = FaseForm()
            try:
                data = form.to_python(data)
                fase = Fase(nombre_fase=data.get('nombre_fase'),tipo_fase=data.get('tipo_fase'),estado=data.get('estado'),linea_base=data.get('linea_base'),descripcion=data.get('descripcion'))
                #if isinstance(fase,Fase) :
                DBSession.add(fase)
                DBSession.flush()
                #DBSession.commit()
                #transaction.commit() 
                print fase
                flash("Fase agregada!")
            except Invalid, e:
                print e
                fase = None
                errors = e.unpack_errors()
                flash(_("Favor complete los datos requeridos"),'warning')
            except IntegrityError:
                flash("LLave duplicada")
                DBSession.rollback()
                redirect('/agregar_fase')
            
        else:
            errors = {}        
        #aqui se debe guardar los datos obtenidos
        #usuario = Usuario(data[0])
        #tmpl = loader.load('agregar_usuario.html')
        #stream = tmpl.generate()
        #return stream.render('html',doctype='html')
        return dict(pagina='agregar_fase',data=data.get('nombre_fase'),errors=errors)

  
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @expose('saip2011.templates.tipo_fase')
    def tipo_fase(self):
        """
           Menu para Tipos de Fase
        """
        return dict(pagina="tipo_fase")
    
    @expose('saip2011.templates.editar_tipo_fase')
    def tipo_fasemod(self,id_tipo_fase,action):
        """
           Metodo que recibe ID de tipos de fases para
           ser modificado
        """
        return "Pagina no disponible"
    
    @expose('saip2011.templates.listar_tipo_fase')
    def listar_tipo_fase(self):
        """Lista tipos de fases 
        """
        tipos_fases = Tipo_Fase.get_tipo_fase()
        return dict(pagina="listar_tipo_fase",tipos_fases=tipos_fases)

    @expose('saip2011.templates.agregar_tipo_fase')
    def agregar_tipo_fase(self,cancel=False,**data):
        errors = {}
        tipo_fase = None
        if request.method == 'POST':
            if cancel:
                redirect('/tipo_fase')
            form = TipoFaseForm()
            try:
                data = form.to_python(data)
                tipo_fase = Tipo_Fase(nombre_tipo_fase=data.get('nombre_tipo_fase'),descripcion=data.get('descripcion'))
                #if isinstance(tipo_fase,Tipo_Fase) :
                DBSession.add(tipo_fase)
                DBSession.flush()
                #DBSession.commit()
                #transaction.commit() 
                print tipo_fase
                flash("Tipo de Fase agregada!")
            except Invalid, e:
                print e
                tipo_fase = None
                errors = e.unpack_errors()
                flash(_("Favor complete los datos requeridos"),'warning')
            except IntegrityError:
                flash("LLave duplicada")
                DBSession.rollback()
                redirect('/agregar_tipo_fase')
            
        else:
            errors = {}        
        #aqui se debe guardar los datos obtenidos
        #usuario = Usuario(data[0])
        #tmpl = loader.load('agregar_usuario.html')
        #stream = tmpl.generate()
        #return stream.render('html',doctype='html')
        return dict(pagina='agregar_tipo_fase',data=data.get('nombre_tipo_fase'),errors=errors)


 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @expose('saip2011.templates.item')
    def item(self):
        """
           Menu para Item
        """
        return dict(pagina="item")
    
    @expose('saip2011.templates.editar_item')
    def itemmod(self,id_item,action):
        """
           Metodo que recibe ID del item para
           ser modificado
        """
        return "Pagina no disponible"
    
    @expose('saip2011.templates.listar_item')
    def listar_item(self):
        """Lista de item 
        """
        items = Item.get_item()
        return dict(pagina="listar_item",items=items)

    @expose('saip2011.templates.agregar_item')
    def agregar_item(self,cancel=False,**data):
        errors = {}
        item = None
        if request.method == 'POST':
            if cancel:
                redirect('/item')
            form = ItemForm()
            try:
                data = form.to_python(data)
                item = Item(nombre_item=data.get('nombre_item'), tipo_item=data.get('tipo_item'), fase=data.get('fase'), proyecto=data.get('proyecto'), adjunto=data.get('adjunto'), estado=data.get('estado'),campos=data.get('campos'),complejidad=data.get('complejidad'), lista_item=data.get('lista_item'),creado_por=data.get('creado_por'),fecha_creacion=data.get('fecha_creacion'))
                #if isinstance(item,Item) :
                DBSession.add(item)
                DBSession.flush()
                #DBSession.commit()
                #transaction.commit() 
                print item
                flash("Item agregado!")
            except Invalid, e:
                print e
                item = None
                errors = e.unpack_errors()
                flash(_("Favor complete los datos requeridos"),'warning')
            except IntegrityError:
                flash("LLave duplicada")
                DBSession.rollback()
                redirect('/agregar_item')
            
        else:
            errors = {}        
        #aqui se debe guardar los datos obtenidos
        #usuario = Usuario(data[0])
        #tmpl = loader.load('agregar_usuario.html')
        #stream = tmpl.generate()
        #return stream.render('html',doctype='html')
        return dict(pagina='agregar_item',data=data.get('nombre_item'),errors=errors)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @expose('saip2011.templates.tipo_item')
    def tipo_item(self):
        """
           Menu para Tipos de Item
        """
        return dict(pagina="tipo_item")
    
    @expose('saip2011.templates.editar_tipo_item')
    def tipo_itemmod(self,id_tipo_item,action):
        """
           Metodo que recibe ID de tipos de item para
           ser modificado
        """
        return "Pagina no disponible"
    
    @expose('saip2011.templates.listar_tipo_item')
    def listar_tipo_item(self):
        """Lista tipos de items 
        """
        tipos_items = Tipo_Item.get_tipo_item()
        return dict(pagina="listar_tipo_item",tipos_items=tipos_items)

    @expose('saip2011.templates.agregar_tipo_item')
    def agregar_tipo_item(self,cancel=False,**data):
        errors = {}
        tipo_item = None
        if request.method == 'POST':
            if cancel:
                redirect('/tipo_item')
            form = TipoItemForm()
            try:
                data = form.to_python(data)
                tipo_item = Tipo_Item(nombre_tipo_item=data.get('nombre_tipo_item'),descripcion=data.get('descripcion'))
                #if isinstance(tipo_item,Tipo_Item) :
                DBSession.add(tipo_item)
                DBSession.flush()
                #DBSession.commit()
                #transaction.commit() 
                print tipo_item
                flash("Tipo de item agregado!")
            except Invalid, e:
                print e
                tipo_item = None
                errors = e.unpack_errors()
                flash(_("Favor complete los datos requeridos"),'warning')
            except IntegrityError:
                flash("LLave duplicada")
                DBSession.rollback()
                redirect('/agregar_tipo_item')
            
        else:
            errors = {}        
        #aqui se debe guardar los datos obtenidos
        #usuario = Usuario(data[0])
        #tmpl = loader.load('agregar_usuario.html')
        #stream = tmpl.generate()
        #return stream.render('html',doctype='html')
        return dict(pagina='agregar_tipo_item',data=data.get('nombre_tipo_item'),errors=errors)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @expose('saip2011.templates.equipo')
    def equipo(self):
        """
           Menu para Equipo de Desarrollo
        """
        return dict(pagina="equipo")
    
    @expose('saip2011.templates.editar_equipo')
    def equipomod(self,id_equipo,action):
        """
           Metodo que recibe ID de equipo para
           ser modificado
        """
        return "Pagina no disponible"
    
    @expose('saip2011.templates.listar_equipo')
    def listar_equipo(self):
        """Lista equipos 
        """
        equipos = Equipo_Desarrollo.get_equipo()
        return dict(pagina="listar_equipo",equipos=equipos)

    @expose('saip2011.templates.agregar_equipo')
    def agregar_equipo(self,cancel=False,**data):
        errors = {}
        equipo = None
        if request.method == 'POST':
            if cancel:
                redirect('/equipo')
            form = EquipoForm()
            try:
                data = form.to_python(data)
                equipo = Privilegios(alias=data.get('alias'),rol=data.get('rol'))
                #if isinstance(usuario,Usuario) :
                DBSession.add(equipo)
                DBSession.flush()
                #DBSession.commit()
                #transaction.commit() 
                print equipo
                flash("Equipo de Desarrollo agregado!")
            except Invalid, e:
                print e
                equipo = None
                errors = e.unpack_errors()
                flash(_("Favor complete los datos requeridos"),'warning')
            except IntegrityError:
                flash("LLave duplicada")
                DBSession.rollback()
                redirect('/agregar_equipo')
            
        else:
            errors = {}        
        #aqui se debe guardar los datos obtenidos
        #usuario = Usuario(data[0])
        #tmpl = loader.load('agregar_usuario.html')
        #stream = tmpl.generate()
        #return stream.render('html',doctype='html')
        return dict(pagina='agregar_equipo',data=data.get('alias'),errors=errors)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @expose('saip2011.templates.proyecto')
    def proyecto(self):
        """
           Menu para Proyecto
        """
        return dict(pagina="proyecto")
    
    @expose('saip2011.templates.editar_proyecto')
    def fasemod(self,id_proyecto,action):
        """
           Metodo que recibe ID de proyecto para
           ser modificado
        """
        return "Pagina no disponible"
    
    @expose('saip2011.templates.listar_proyecto')
    def listar_proyecto(self):
        """Lista proyectos 
        """
        proyectos = Proyecto.get_proyecto()
        return dict(pagina="listar_proyecto",proyectos=proyectos)

    @expose('saip2011.templates.agregar_proyecto')
    def agregar_proyecto(self,cancel=False,**data):
        errors = {}
        proyecto = None
        if request.method == 'POST':
            if cancel:
                redirect('/proyecto')
            form = ProyectoForm()
            try:
                data = form.to_python(data)
                proyecto = Proyecto(nombre_proyecto=data.get('nombre_proyecto'),equipo=data.get('equipo'),lista_Fases=data.get('lista_Fases'),descripcion=data.get('descripcion'))
                #if isinstance(proyecto,Proyecto) :
                DBSession.add(proyecto)
                DBSession.flush()
                #DBSession.commit()
                #transaction.commit() 
                print proyecto
                flash("Proyecto agregado!")
            except Invalid, e:
                print e
                proyecto = None
                errors = e.unpack_errors()
                flash(_("Favor complete los datos requeridos"),'warning')
            except IntegrityError:
                flash("LLave duplicada")
                DBSession.rollback()
                redirect('/agregar_proyecto')
            
        else:
            errors = {}        
        #aqui se debe guardar los datos obtenidos
        #usuario = Usuario(data[0])
        #tmpl = loader.load('agregar_usuario.html')
        #stream = tmpl.generate()
        #return stream.render('html',doctype='html')
        return dict(pagina='agregar_proyecto',data=data.get('nombre_proyecto'),errors=errors)


