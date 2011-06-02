# -*- coding: utf-8 -*-
"""
Fase* related model.


It's perfectly fine to re-use this definition in the Saip application,
though.

"""
import os
from datetime import datetime
import sys

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime , Text , String
from sqlalchemy.orm import relation, synonym

from saip2011.model import DeclarativeBase, metadata, DBSession

from saip2011.model.proyecto import Proyecto , tabla_proyecto_fases

__all__ = ['Fase']


class Fase(DeclarativeBase):
	"""
	Definicion de Fase.

	"""

	__tablename__ = 'Tabla_Fase'

	#{ Columns

	idfase = Column(Integer, autoincrement=True, primary_key=True)

	nombrefase = Column(Unicode(30), unique=True, nullable=False)

	estado = Column(Unicode(30), nullable=False)
	
	descripcion = Column(Text)

	#{ Relations   /// se indica quien me va a usar
    
	listafases = relation(Proyecto, secondary=tabla_proyecto_fases, backref='Lista_de_Fases')

	
	#{ Special methods

	def __repr__(self):
		return '<Fase: Nombre=%s>' % self.nombrefase
	
	def __unicode__(self):
		return self.nombrefase

	#}

