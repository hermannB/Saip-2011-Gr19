# -*- coding: utf-8 -*-
"""
Adjunto* related model.

"""
import os
from datetime import datetime
import sys

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, Text
from sqlalchemy.orm import relation, synonym

from saip2011.model import DeclarativeBase, metadata, DBSession
from saip2011.model.item import Item,tabla_item_adjunto

__all__ = ['Adjunto']


class Adjunto(DeclarativeBase):
	"""
	Definicion de Adjunto
	"""

	__tablename__ = 'Tabla_Adjunto'

	#{ Columns

	idadjunto = Column(Integer, autoincrement=True, primary_key=True)

	text = Column(Text, nullable=False)

	#{ Relations   /// se indica quien me va a usar

	items = relation(Item, secondary= tabla_item_adjunto, backref='Adjunto')


	#{ Special methods

	def __repr__(self):
		return '<Adjunto: id=%s>' % self.idadjunto

	def __unicode__(self):
		return self.idadjunto
	#}

