# -*- coding: utf-8 -*-
"""
ITEM* related model.

This is where the models used by :mod:`repoze.who` and :mod:`repoze.what` are
defined.

It's perfectly fine to re-use this definition in the Saip application,
though.

"""

import os
from datetime import datetime
import sys

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime , Text
from sqlalchemy.orm import relation, synonym
from saip2011.model.tipo_item import Tipo_Item
from saip2011.model.variables import Variables
from saip2011.model import DeclarativeBase, metadata, DBSession

__all__ = ['Item']

relaciones_item_tabla = Table('Tabla_Relaciones_Item', metadata,
    Column('id_relacion', Integer, ForeignKey('Tabla_Relaciones.id_relacion',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('id_item', Integer, ForeignKey('Tabla_Item.id_item',
        onupdate="CASCADE", ondelete="CASCADE"))
)

linea_base_item_tabla = Table('Tabla_Linea_Base_Item', metadata,
    Column('id_linea_base', Integer, ForeignKey('Tabla_Linea_Base.id_linea_base',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('id_item', Integer, ForeignKey('Tabla_Item.id_item',
        onupdate="CASCADE", ondelete="CASCADE"))
)

################################################################################

class Item(DeclarativeBase):
    """
    Definicion Item
    """

    __tablename__ = 'Tabla_Item'


    #           Columnas

    id_item = Column(Integer, autoincrement=True, primary_key=True)

    nombre_item = Column(Unicode(50), nullable=False)

    codigo_item = Column(Unicode(50), nullable=False)		

    id_tipo_item = Column(Integer, ForeignKey('Tabla_Tipo_Item.id_tipo_item'))

    nombre_tipo_item = relation('Tipo_Item', backref='Item')

    fase = Column(Integer, nullable=False)

    orden = Column(Integer, nullable=False)

    proyecto = Column(Integer, nullable=False)

    complejidad = Column(Integer, nullable=False)

    estado = Column(Unicode(50), nullable=False)

    estado_oculto = Column(Unicode(50), nullable=False)

    lb_general = Column(Integer, nullable=False)
    
    lb_parcial = Column(Integer, nullable=False)

    version = Column(Integer)

    creado_por = Column(Unicode(50), nullable=False)

    fecha_creacion = Column(DateTime, default=datetime.now)

################################################################################

    #               Metodos

    def __repr__(self):
        return '<Item: Id Item=%s>' % self.id_item

    def __unicode__(self):
        return self.id_item

#-------------------------------------------------------------------------------

    @classmethod
    def get_ultimo_id(self):
        """
        Obtiene el ultimo id de la tabla Item.
        """

        mayor =0
        items = DBSession.query(Item).all()
        for item in items:
            if (item.id_item > mayor):
	            mayor =item.id_item
        return mayor

    print get_ultimo_id.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_item_by_id(self, id_item):
        """
        Obtiene item uscado por su identificador.
        """

        item = DBSession.query(Item).get(int(id_item))
        return item

    print get_item_by_id.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_master(self):
        """
        Obtiene item maestro.
        """
        items = DBSession.query(Item).all()

        for item in items:
            if item.nombre_item=="master":
                return item

    print get_master.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_item_proy_fase(self,proy,fase):
        """
        Obtiene la lista de los items por proyecto y fase.
        """

        lista=[]
        items = DBSession.query(Item).all()

        for item in items:
            if( item.estado_oculto=="Activo" and item.proyecto == proy
                and item.fase == fase):
                lista.append(item)  

        return lista

    print get_item_proy_fase.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_item_activados(self):
        """
        Obtiene la lista de todos los items en estado ACTIVO.
        """

        lista=[]
        items = DBSession.query(Item).all()
        for item in items:
            if( item.estado_oculto=="Activo"):
                lista.append(item)  

        return lista

    print get_item_activados.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_nombres_items(self):
        """
        Obtiene la lista de los nombres de los items
        """

        fase=int(Variables.get_valor_by_nombre("fase_actual"))
        items = Item.get_item_activados_by_fase(fase)
        lista=[]
        for item in items:
            if( item.estado_oculto=="Activo"):
                lista.append(item.nombre_item)  

        return lista

    print get_nombres_items.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_item_activados_by_fase(self,fase):
        """
        Obtiene la lista de todos los items activos de una determinada fase.
        """

        proyecto=int(Variables.get_valor_by_nombre("proyecto_actual"))
        lista=[]
        items = DBSession.query(Item).all()

        for item in items:
            if( item.estado_oculto=="Activo" and item.proyecto == proyecto
                and item.fase == int(fase)):
                lista.append(item)  

        return lista

    print get_item_activados_by_fase.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_item_activados_by_fase_por_pagina(self,fase,start=0,end=5):
        """
        Obtiene la lista de todos los items activos de una determinada fase.
        """

        id_proyecto=int(Variables.get_valor_by_nombre("proyecto_actual"))
        items = DBSession.query(Item).slice(start,end).all()
        
        lista=[]
        for item in items:
            if( item.estado_oculto=="Activo" and item.proyecto == id_proyecto
                and item.fase == int(fase)):
                lista.append(item)

        return lista

    print get_item_activados_by_fase_por_pagina.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_item_activados_by_fase_por_filtro(self,id_fase,param,texto):
        """
        Obtiene la lista de todos los items activos de una fase. Los items se buscan por 'nombre' y 'estadp'
        """

        id_proyecto=int(Variables.get_valor_by_nombre("proyecto_actual"))
        
        if param == "nombre":
            items = DBSession.query(Item).filter(Item.nombre_item.like('%s%s%s' % ('%',texto,'%'))).all()
        elif param == "estado":
            items = DBSession.query(Item).filter(Item.estado.like('%s%s%s' % ('%',texto,'%'))).all()
        
        lista=[]
        for item in items:
            if( item.estado_oculto=="Activo" and item.proyecto == id_proyecto
                and item.fase == int(id_fase)):
                lista.append(item)

        return lista

    print get_item_activados_by_fase_por_filtro.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def crear_codigo(self,id_tipo,pre_codigo,proy_actual,fas_act):
        """
        Crea el codigo del item.
        """

        codigo=""
        cantidad=1
        tipo = DBSession.query(Tipo_Item).get(id_tipo)
        items = DBSession.query(Item).all()

        codigo+=pre_codigo+"-"

        for i in items:
            if (i.id_tipo_item == id_tipo and i.proyecto == proy_actual
                and i.fase == fas_act):
                cantidad=cantidad+1
                codigo+=str(cantidad)
        return codigo

    print crear_codigo.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_item_eliminados(self):
        """
        Obtiene la lista de todos los items eliminados.
        """

        lista=[]
        items = DBSession.query(Item).all()

        for item in items:
            if( item.estado_oculto=="Eliminado"):
                lista.append(item)  

        return lista

    print get_item_eliminados.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_item_eliminados_by_fase(self,fase):
        """
        Obtiene la lista de todos los items eliminados de una fase.
        """

        proyecto=int(Variables.get_valor_by_nombre("proyecto_actual"))
        lista=[]
        items = DBSession.query(Item).all()
        for item in items:
            if( item.estado_oculto=="Eliminado"and item.proyecto == proyecto
                and item.fase == int(fase)):
                lista.append(item)  

        return lista

    print get_item_eliminados_by_fase.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_item_eliminados_por_pagina(self,id_fase,start=0,end=5):
        """
        Obtiene la lista de todos los items eliminados de una fase.
        """

        id_proyecto=int(Variables.get_valor_by_nombre("proyecto_actual"))
        item = DBSession.query(Item).slice(start,end).all()
        lista=[]
        for item in items:
            if( item.estado_oculto=="Eliminado" and item.proyecto == proy
                and item.fase == fase):
                lista.append(item)

        return lista

    print get_item_eliminados_por_pagina.__doc__

#-------------------------------------------------------------------------------


    @classmethod
    def get_historial(self, id_item):
        """
        Obtiene el historial de un item.
        """

        muestra=DBSession.query(Item).get(id_item)
        lista=[]
        items = DBSession.query(Item).all()

        for item in items:
            if( (item.proyecto== muestra.proyecto)and(item.fase == muestra.fase) 
                and ( item.codigo_item ==muestra.codigo_item) and
                (item.estado_oculto == "Desactivado") ):
                lista.append(item)  

        return lista

    print get_historial.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_historial_por_pagina(self,id_item,start=0,end=5):
        """
        Obtiene el historial de un item.
        """

        id_proyecto=int(Variables.get_valor_by_nombre("proyecto_actual"))
        item = DBSession.query(Item).slice(start,end).all()
        lista=[]

        for item in items:
            if( (item.proyecto== muestra.proyecto)and(item.fase == muestra.fase) 
		        and ( item.codigo_item ==muestra.codigo_item) and
                (item.estado_oculto == "Desactivado") ):
                lista.append(item)

        return lista

    print get_historial_por_pagina.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def version_actual(self, id_item):
        """
        Obtiene la versión actual de un item
        """

        items = Item.get_item_activados()
        item_viejo = DBSession.query(Item).get(id_item)

        for item in items:
            if( (item.nombre_item == item_viejo.nombre_item) and  
                (item.proyecto == item_viejo.proyecto)  and 
                (item.fase == item_viejo.fase ) ):
                return item

    print version_actual.__doc__ 

#-------------------------------------------------------------------------------
         
    @classmethod
    def activar(self, id_item):
        """
        Activa un item.
        """

        item = DBSession.query(Item).get(id_item)
        if item.estado == "nuevo":
            item.estado="en_desarrollo"
            DBSession.flush()

    print activar.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def aprobar(self, id_item):
        """
        Aprueba un item en estado en desarrollo.
        """

        item = DBSession.query(Item).get(id_item)
        if item.estado == "en_desarrollo":
            item.estado="aprobado"
            DBSession.flush()

    print aprobar.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def con_linea_base(self, id_item):
        """
        Se asigna al item como parte de la linea base.
        """

        item = DBSession.query(Item).get(id_item)
        if item.estado == "aprobado":
            item.estado="con_linea_base"
            DBSession.flush()

    print con_linea_base.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def revisar(self, id_item):
        """
        El item se pasa al estado 'a revisar'.
        """

        item = DBSession.query(Item).get(id_item)
        if item.estado == "aprobado" or item.estado == "con_linea_base":
            item.estado="a_revisar"
            DBSession.flush()

    print revisar.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def finalizar(self, id_item):
        """
        
        """
        proyecto = DBSession.query(Item).get(id_item)
        if item.estado == "con_linea_base":
            item.estado="finalizado"
            DBSession.flush()

    print finalizar.__doc__

#-------------------------------------------------------------------------------
    @classmethod
    def borrar_by_id(self,id_item):
        """
        Eliina un item específico.         
        """

        DBSession.delete(DBSession.query(Item).get(id_item))
        DBSession.flush()

    print borrar_by_id.__doc__

#-------------------------------------------------------------------------------
################################################################################
