# -*- coding: utf-8 -*-
"""
Auth* related model.

This is where the models used by :mod:`repoze.who` and :mod:`repoze.what` are
defined.

It's perfectly fine to re-use this definition in the Saip application,
though.

"""
import os
from datetime import datetime
import sys

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime , Text , Enum
from sqlalchemy.orm import relation, synonym

from saip2011.model import DeclarativeBase, metadata, DBSession

__all__ = ['Item']

tabla_item_adjunto = Table('TB_item_adjunto', metadata,
	Column('iditem', Integer, ForeignKey('Tabla_Item.iditem', onupdate="CASCADE", ondelete="CASCADE")),
	Column('idadjunto', Integer, ForeignKey('Tabla_Adjunto.idadjunto', onupdate="CASCADE", ondelete="CASCADE"))
)


class Item(DeclarativeBase):
	"""
	Definicion Item
	"""

	__tablename__ = 'Tabla_Item'

	#{ Columns
	
	iditem = Column(Integer, autoincrement=True, primary_key=True)

	tipo_id = Column('nombretipo', Unicode(30), ForeignKey('Tabla_TipoItem.nombretipo'))

	tipoitem = relation('TipoItem', backref='itemm')

	fase = Column(Unicode(30) ,  nullable=False)

	proyecto = Column(Unicode(30), nullable=False)

	adjunto = Column(Integer)

	complejidad = Column(Integer, nullable=False)

	estado = Column(Unicode(30), nullable=False)

	campos = Column(Text, nullable=False)

	listaitem = Column(Text)

	creadopor = Column(Unicode(30), nullable=False)

	fechacreacion = Column(DateTime, default=datetime.now)
	
	#{ Special methods
	
			
	def __repr__(self):
		return '<Item: Id Item=%s>' % self.iditem

	def __unicode__(self):
		return self.iditem

	#}


