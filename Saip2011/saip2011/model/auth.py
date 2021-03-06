# -*- coding: utf-8 -*-
"""
Auth* related model.

This is where the models used by :mod:`repoze.who` and :mod:`repoze.what` are
defined.

It's perfectly fine to re-use this definition in the Saip2011 application,
though.

"""

import os
from datetime import datetime
import transaction
import sys
try:
    from hashlib import sha1
except ImportError:
    sys.exit('ImportError: No module named hashlib\n'
             'If you are on python2.4 this library is not part of python. '
             'Please install it. Example: easy_install hashlib')

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime , Text
from sqlalchemy.orm import relation, synonym

from saip2011.model import DeclarativeBase, metadata, DBSession

__all__ = ['Usuario', 'Rol', 'Privilegios']


################################################################################

#               Tablas Intermedias para relaciones muchos a muchos


# Tabla rol - Privilegio

rol_privilegio_tabla = Table('Tabla_Rol_Privilegios', metadata,
    Column('rol_id', Integer, ForeignKey('Tabla_Rol.idrol',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('privilegio_id',Integer, ForeignKey('Tabla_Privilegios.idprivilegio',
        onupdate="CASCADE", ondelete="CASCADE"))
)

# Tabla Usuario - Rol

usuario_rol_tabla = Table('Tabla_Usuario_Rol', metadata,
    Column('usuario_id', Integer, ForeignKey('Tabla_Usuario.idusuario',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('rol_id', Integer, ForeignKey('Tabla_Rol.idrol',
        onupdate="CASCADE", ondelete="CASCADE"))
)

################################################################################


class Rol(DeclarativeBase):
    """
    Definición de Rol

    """

    __tablename__ = 'Tabla_Rol'

    #              Columnas

    idrol = Column(Integer, autoincrement=True, primary_key=True)

    nombrerol = Column(Unicode(50), unique=True, nullable=False)

    descripcion = Column(Text)

################################################################################
    
    #               Metodos

    def __repr__(self):
        return '<Rol: nombre=%s>' % self.nombrerol

    def __unicode__(self):
        return self.nombrerol

#-------------------------------------------------------------------------------

    @classmethod
    def get_roles(self):
        """
        Obtiene la lista de todos los roles
        registrados en el sistema
        """
        """roles = session.query(cls).all()"""

        roles = DBSession.query(Rol).all()
            
        return roles

    print get_roles.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_nombreroles(self):
        """
        Obtiene los nombres de los roles.
        """

        roles = DBSession.query(Rol).all()
        lista=[]

        for rol in roles:
            lista.append(rol.nombrerol)    

        return lista

    print get_nombreroles.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_rol_by_nombre(self,nombre):
        """
        Obtiene el rol buscado por su nombre
        """
        """roles = session.query(cls).all()"""

        roles = DBSession.query(Rol).all()

        for rol in roles:
            if rol.nombrerol == str(nombre): 
                return rol

    print get_rol_by_nombre.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_rol_by_id(self,id_rol):
        """
        Obtiene el rol por medio de su identificador de rol
        """
        """roles = session.query(cls).all()"""
        roles = DBSession.query(Rol).all()

        for rol in roles:
            if rol.idrol == id_rol: 
                return rol

    print get_rol_by_id.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_roles_por_pagina(self,start=0,end=5):
        """
        Obtiene la lista de todos los roles
        registrados en el sistema
        """
        """roles = session.query(cls).all()"""

        roles = DBSession.query(Rol).slice(start,end).all()
            
        return roles

    print get_roles_por_pagina.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_roles_por_filtro(self,param,texto,start=0,end=5):
        """
        Obtiene la lista de todos los roles bsucados por 'nombre' o 'descripcion'
        """
        """usuarios = session.query(cls).all()"""

        if param == "nombre":
            roles = DBSession.query(Rol).filter(Rol.nombrerol.like('%s%s%s' % ('%',texto,'%'))).all()
        elif param == "descripcion":
            roles = DBSession.query(Rol).filter(Rol.descripcion.like('%s%s%s' % ('%',texto,'%'))).all()
            
        return roles

    print get_roles_por_filtro.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def borrar_by_id(self,id_rol):
        """
        Elimina el rol         
        """

        DBSession.delete(DBSession.query(Rol).get(id_rol))
        DBSession.flush()

    print borrar_by_id.__doc__	

#-------------------------------------------------------------------------------

    #                   Relaciones
    
    usuarios = relation('Usuario', secondary=usuario_rol_tabla,backref='roles')
    

################################################################################
        



# The 'info' argument we're passing to the email_address and password columns
# contain metadata that Rum (http://python-rum.org/) can use generate an
# admin interface for your models.

class Usuario(DeclarativeBase):
    """
    User definition.

    This is the user definition used by :mod:`repoze.who`, which requires at
    least the ``user_name`` column.

    """

    __tablename__ = 'Tabla_Usuario'

                #       Columnas

    idusuario = Column(Integer, autoincrement=True, primary_key=True)

    alias = Column(Unicode(50), unique=True, nullable=False)

    nombre = Column(Unicode(50), nullable=False)

    apellido = Column(Unicode(50), nullable=False)

    _password = Column('password', Unicode(80),
                                        info={'rum': {'field':'Password'}})

    email_address = Column(Unicode(50),  nullable=False, 
                                            info={'rum': {'field':'Email'}})

    nacionalidad = Column(Unicode(50))

    tipodocumento = Column(Unicode(50), nullable=True)

    nrodoc = Column(Integer, nullable=True)

    ################################################################################

    #               Metodos

    def __repr__(self):
        return '<User: email="%s", Alias="%s">' % (self.email_address, 
                                                        self.alias)

    def __unicode__(self):
        return self.alias

    #-------------------------------------------------------------------------------

    @property
    def privilegios(self):
        """Retorna un conjunto de strings para los permisos granteados."""

        perms = set()
        for g in self.roles:
            perms = perms | set(g.privilegios)

        return perms

    print privilegios.__doc__

    #-------------------------------------------------------------------------------

    @classmethod
    def by_email_address(cls, email):
        """Return the user object whose email address is ``email``."""

        return DBSession.query(cls).filter(cls.email_address==email).first()

    #-------------------------------------------------------------------------------

    @classmethod
    def by_alias(cls, username):

        """Return the user object whose user name is ``username``."""

        return DBSession.query(cls).filter(cls.alias==username).first()

    #-------------------------------------------------------------------------------


    def _set_password(self, password):
        """Hash ``password`` on the fly and store its hashed version."""
        hashed_password = password
        
        if isinstance(password, unicode):
            password_8bit = password.encode('UTF-8')
        else:
            password_8bit = password

        salt = sha1()
        salt.update(os.urandom(60))
        hash = sha1()
        hash.update(password_8bit + salt.hexdigest())
        hashed_password = salt.hexdigest() + hash.hexdigest()

        # Make sure the hashed password is an UTF-8 object at the end of the
        # process because SQLAlchemy _wants_ a unicode object for Unicode
        # columns
        if not isinstance(hashed_password, unicode):
            hashed_password = hashed_password.decode('UTF-8')

        self._password = hashed_password

    #-------------------------------------------------------------------------------


    def _get_password(self):
        """Return the hashed version of the password."""

        return self._password

    password = synonym('_password', descriptor=property(_get_password,
                                                        _set_password))


    #-------------------------------------------------------------------------------


    def validate_password(self, password):
        """
        Check the password against existing credentials.
        
        :param password: the password that was provided by the user to
            try and authenticate. This is the clear text version that we will
            need to match against the hashed one in the database.
        :type password: unicode object.
        :return: Whether the password is valid.
        :rtype: bool

        """
        hashed_pass = sha1()
        hashed_pass.update(password + self.password[:40])
        return self.password[40:] == hashed_pass.hexdigest()

    #-------------------------------------------------------------------------------

    @classmethod
    def get_usuarios(self):

        """
        Obtiene la lista de todos los usuarios
        registrados en el sistema
        """
        """usuarios = session.query(cls).all()"""

        usuarios = DBSession.query(Usuario).all()

        return usuarios

    print get_usuarios.__doc__

    #-------------------------------------------------------------------------------

    @classmethod
    def get_usuarios_por_pagina(self,start=0,end=5):
        """
        Obtiene la lista de todos los usuarios
        registrados en el sistema
        """
        """usuarios = session.query(cls).all()"""

        usuarios = DBSession.query(Usuario).slice(start,end).all()
            
        return usuarios

    print get_usuarios_por_pagina.__doc__

    #-------------------------------------------------------------------------------

    @classmethod
    def get_usuarios_por_filtro(self,param,texto,start=0,end=5):
        """
        Obtiene la lista de usuarios buscados por 'alias', 'nombre' y  'apellido'
        registrados en el sistema
        """
        """usuarios = session.query(cls).all()"""

        if param == "alias":
            usuarios = DBSession.query(Usuario).filter(Usuario.alias.like('%s%s%s' % ('%',texto,'%'))).all()
        elif param == "nombre":
            usuarios = DBSession.query(Usuario).filter(Usuario.nombre.like('%s%s%s' % ('%',texto,'%'))).all()
        elif param == "apellido":
            usuarios = DBSession.query(Usuario).filter(Usuario.apellido.like('%s%s%s' % ('%',texto,'%'))).all()
            
        return usuarios

    print get_usuarios_por_filtro.__doc__

    #-------------------------------------------------------------------------------

    @classmethod
    def get_alias(self):
        """
        Obtiene la lista de todos los alias de los usuarios
        registrados en el sistema
        """

        usuarios = DBSession.query(Usuario).all()
        lista=[]

        for usuario in usuarios:
            lista.append(usuario.alias)    

        return lista

    print get_alias.__doc__

    #-------------------------------------------------------------------------------

    @classmethod
    def get_user_by_alias(self,name):
        """
        Obtiene el usuario por medio del alias pasado como parámetro.
        """

        usuarios = DBSession.query(Usuario).all()
        for usuario in usuarios:    
            if (usuario.alias==name):	
                    return usuario

    print get_user_by_alias.__doc__

    #-------------------------------------------------------------------------------

    @classmethod
    def get_user_by_id(self, iduser):
        """
        Obtiene el usuario por su id
        """

        usuario = DBSession.query(Usuario).filter_by(idusuario=iduser).first()
        return usuario

    print get_user_by_id.__doc__

    #-------------------------------------------------------------------------------

    @classmethod
    def borrar_by_id(self,iduser):
        """
        Elimina el usuario dado.
        """

        DBSession.delete(DBSession.query(Usuario).get(iduser))
        DBSession.flush()	

    #-------------------------------------------------------------------------------

    @classmethod
    def get_usuarios_por_pagina(self,start=0,end=5):
        """
        Obtiene la lista de todos los usuarios
        registrados en el sistema
        """
        """usuarios = session.query(cls).all()"""

        usuarios = DBSession.query(Usuario).slice(start,end).all()
            
        return usuarios

    print get_usuarios_por_pagina.__doc__

#-------------------------------------------------------------------------------

################################################################################

class Privilegios(DeclarativeBase):
    """
    Permission definition for :mod:`repoze.what`.

    Only the ``permission_name`` column is required by :mod:`repoze.what`.

    """

    __tablename__ = 'Tabla_Privilegios'

    #               Columnas

    idprivilegio = Column(Integer, autoincrement=True, primary_key=True)

    nombreprivilegio = Column(Unicode(50), unique=True, nullable=False)

    var = Column(Unicode(50))

    descripcion = Column(Text)

################################################################################

    #               Relaciones
    
    roles = relation(Rol, secondary=rol_privilegio_tabla,
                      backref='privilegios')

################################################################################
    
    #               Metodos
    
    def __repr__(self):
        return '<Privilegio: nombre=%s>' % self.nombreprivilegio

    def __unicode__(self):
        return self.nombreprivilegio

#-------------------------------------------------------------------------------
    
    @classmethod
    def get_privilegios(self):
        """
        Obtiene la lista de todos los privilegios
        """
        """privilegios = session.query(cls).all()"""

        privilegios = DBSession.query(Privilegios).all()
        return privilegios

    print get_privilegios.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_privilegio_por_pagina(self,start=0,end=5):
        """
        Obtiene la lista de todos los privilegios
        """
        """privilegios = session.query(cls).all()"""
        #privilegios = DBSession.query(Privilegios).all()
        privilegios = DBSession.query(Privilegios).slice(start,end).all()
            
        return privilegios

    print get_privilegio_por_pagina.__doc__

#-------------------------------------------------------------------------------
    
    @classmethod
    def get_privilegio_por_filtro(self,param,texto,start=0,end=5):
        """
        Obtiene la lista de los privilegios buscados por 'nombre' o 'descripción'
        """
        """privilegios = session.query(cls).all()"""
        #privilegios = []
        
        if param == "nombre":
            privilegios = DBSession.query(Privilegios).filter(Privilegios.nombreprivilegio.like('%s%s%s' % ('%',texto,'%'))).all()
            
        elif param == "descripcion":
            privilegios = DBSession.query(Privilegios).filter(Privilegios.descripcion.like('%s%s%s' % ('%',texto,'%'))).all()
              
           
        return privilegios

    print get_privilegio_por_filtro.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_nombreprivilegios(self):
        """
        Obtiene los nombres de los privilegios.
        """

        privilegios = DBSession.query(Privilegios).all()
        lista=[]
        for privilegio in privilegios:
            lista.append(privilegio.nombreprivilegio)    

        return lista

    print get_nombreprivilegios.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_privilegio_by_id(self,idprivilegio):
        """
        Obtiene el privilegio a través de su idenf¡tificador de privilegio.
        """

        privilegio = DBSession.query(Privilegios).get(int(idprivilegio))
        return privilegio

    print get_privilegio_by_id.__doc__

#-------------------------------------------------------------------------------
    @classmethod
    def borrar_by_id(self,idprivilegio):
        """
        Borra un privilegio.
        """

        DBSession.delete(DBSession.query(Privilegios).get(idprivilegio))
        DBSession.flush()
    
    print borrar_by_id.__doc__

#-------------------------------------------------------------------------------
    @classmethod
    def get_privilegio_por_pagina(self,start=0,end=5):
        """
        Obtiene la lista de todos los Privilegios.
        """
        """privilegios = session.query(cls).all()"""
        #privilegios = DBSession.query(Privilegios).all()
        privilegios = DBSession.query(Privilegios).slice(start,end).all()
            
        return privilegios

    print get_privilegio_por_pagina.__doc__

#-------------------------------------------------------------------------------
