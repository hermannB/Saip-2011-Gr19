# -*- coding: utf-8 -*-
"""
Usuario* related model.

This is where the models used by :mod:`repoze.who` and :mod:`repoze.what` are
defined.

It's perfectly fine to re-use this definition in the Saip application,
though.

"""
import os
from datetime import datetime
import sys
try:
    from hashlib import sha1
except ImportError:
    sys.exit('ImportError: No module named hashlib\n'
             'If you are on python2.4 this library is not part of python. '
             'Please install it. Example: easy_install hashlib')

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime
from sqlalchemy.orm import relation, synonym
from sqlalchemy.orm import sessionmaker

from saip2011.model import DeclarativeBase, metadata, DBSession

__all__ = ['Usuario']


# The 'info' argument we're passing to the email_address and password columns
# contain metadata that Rum (http://python-rum.org/) can use generate an
# admin interface for your models.

class Usuario(DeclarativeBase):
	"""
		Definicion usuario.

		This is the user definition used by :mod:`repoze.who`, which requires at
		least the ``alias`` column.

	"""
    __tablename__ = 'Tabla_Usuario'

	#{ Columns

	idusuario = Column(Integer, autoincrement=True, primary_key=True)
	alias = Column(Unicode(30), unique=True, nullable=False)
	nombre = Column(Unicode(30), nullable=False)
	apellido = Column(Unicode(30), nullable=False)
	_password = Column('password', Unicode(80),info={'rum': {'field':'Password'}},default=12345)

	email_address = Column(Unicode(80), unique=True, nullable=False, info={'rum': {'field':'Email'}},default=alguien@algo.com)

	nacionalidad = Column(Unicode(30),default=Paraguaya)
	tipodocumento = Column(Unicode(30), default=C.I )
	nrodoc = Column(Integer, unique=True, default=00000000)

	#{ Special methods

	def __init__(self, alias, nombre, apellido,_password='12345',email_address='0',nacionalidad='paraguaya',tipodocumento='CI',nrodoc='0'):
		self.alias = alias
		self.nombre = nombre
		self.apellido = apellido
		self._password = _password
		self.email_address = email_address
		self.nacionalidad = nacionalidad
		self.tipodocumento = tipodocumento
		self.nrodoc = nrodoc
        
	@classmethod
	def get_usuarios(self,modelo):
		"""
		Obtiene la lista de todos los usuarios
		registrados en el sistema
		"""
		#Session = sessionmaker()
		#session = Session() 
		"""usuarios = session.query(cls).all()"""
		usuarios = DBSession.query(modelo).all()
		    
		return usuarios

	@classmethod
	def get_usuario_by_id(self,modelo,iduser):
		"""
		   Retorna el usuario con el id especificado
		"""
		Session = sessionmaker()
		session = Session() 
		    #usuario = session.query(cls).all()"""
		usuario = DBSession.query(modelo).filter_by(idusuario=iduser).first()
		    
		return usuario
	    
	def get_url_usuario(self):
		#usuario = DBSession.query(Usuario).filter_by    (idusuario=self.idusuario)
		url = u'self.idusuario'
		return url

	def get_next_id(self):
		for user, in DBSession.query(Usuario.idusuario).desc(idusuario).first():
			print user
            
        	return user

	def __repr__(self):
		return '<User: email="%s", Alias="%s">' % (self.email_address, self.alias)

	def __unicode__(self):
        	return self.alias
    

	@classmethod
	def by_email_address(cls, email):
		"""Return the user object whose email address is ``email``."""
		return DBSession.query(cls).filter(cls.email_address==email).first()

	@classmethod
	def by_alias(cls, apodo):
		"""Return the user object whose user name is ``alias``."""
		return DBSession.query(cls).filter(cls.alias==apodo).first()

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

	def _get_password(self):
		"""Return the hashed version of the password."""
		return self._password

	password = synonym('_password', descriptor=property(_get_password,
                                                        _set_password))
    
    #}
    
	def validate_password(self, password):
		"""
		Check the password against existing credentials.

		 try and authenticate. This is the clear text version that we will
			    need to match against the hashed one in the database.
			:type password: unicode object.
			:return: Whether the password is valid.
			:rtype: bool

			"""
		hashed_pass = sha1()
		hashed_pass.update(password + self.password[:40])
		return self.password[40:] == hashed_pass.hexdigest()

