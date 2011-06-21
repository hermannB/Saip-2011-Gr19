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
from saip2011.model.equipo_desarrollo import Equipo_Desarrollo
from saip2011.model.equipo_desarrollo import equipo_fases_tabla
from saip2011.model.tipo_item import Tipo_Item , fase_tipo_item_tabla
from saip2011.model.item import Item , relaciones_item_tabla

# Import graphviz
import sys
sys.path.append('..')
sys.path.append('/usr/lib/graphviz/python/')
sys.path.append('/usr/lib64/graphviz/python/')
import gv

# Import pygraph
from pygraph.classes.graph import graph
from pygraph.classes.digraph import digraph
from pygraph.algorithms.searching import breadth_first_search
from pygraph.readwrite.dot import write




################################################################################

class Relaciones(DeclarativeBase):
    """
    Definicion de Fase.

    """

    __tablename__ = 'Tabla_Relaciones'

    #               Columnas

    id_relacion = Column(Integer, autoincrement=True, primary_key=True)

    id_item_hijo = Column(Integer, nullable=False)

    padres = relation(Item, secondary=relaciones_item_tabla,
                      backref='items')
################################################################################

    #                   Metodos

    def __repr__(self):
        return '<Relacion: id=%s>' % self.id_relacion

    def __unicode__(self):
        return self.id_relacion

#-------------------------------------------------------------------------------
       
    @classmethod
    def get_relaciones(self):
        """
        Obtiene la lista de todos los usuarios
        registrados en el sistema
        """
        relaciones = DBSession.query(Relaciones).all()
        return relaciones

#-------------------------------------------------------------------------------

    @classmethod
    def get_relacion_by_id(self,rel_id):
        """
        Obtiene la lista de todos los usuarios
        registrados en el sistema
        """
        relacion = DBSession.query(Relaciones).get(int(rel_id))
        return relacion

#-------------------------------------------------------------------------------

    @classmethod
    def get_mis_padres(self,id_item):
        """
        Obtiene la lista de todos los usuarios
        registrados en el sistema
        """
        relaciones = DBSession.query(Relaciones).all()
        lista =[]
        for rel in relaciones:
            if rel.id_item_hijo == id_item:
                for padre in rel.padres:
                    if (padre.estado_oculto=="Activo"):
                        lista.append(padre) 

        return lista

#-------------------------------------------------------------------------------

    @classmethod
    def get_mis_id_hijos(self,id_item):
        """
        Obtiene la lista de todos los usuarios
        registrados en el sistema
        """
        relaciones = DBSession.query(Relaciones).all()
        lista =[]
        for rel in relaciones:
            for padre in rel.padres:
                if (padre.estado_oculto=="Activo"):
                    if padre.id_item == id_item:
                        lista.append(rel.id_item_hijo)
                        break 

        return lista

#-------------------------------------------------------------------------------

    @classmethod
    def get_antecesores(self,id_item):
        """
        Obtiene la lista de todos los usuarios
        registrados en el sistema
        """
        relaciones = DBSession.query(Relaciones).all()
        lista =[]
        padres =[]

        for rel in relaciones:
            if rel.id_item_hijo == id_item:
                for padre in rel.padres:
                    if (padre.estado_oculto=="Activo"):
                        lista.append(padre) 
                        padres.append(padre)

        while len(lista)>0:
            mis_padres=Relaciones.get_mis_padres(int(lista[0].id_item))
            del lista[0]
            for padre in mis_padres:
                if padre not in lista and (padre.estado_oculto=="Activo"):
                    lista.append(padre) 
                    padres.append(padre)
            

        return padres

#-------------------------------------------------------------------------------

    @classmethod
    def get_sucesores(self,id_item):
        """
        Obtiene la lista de todos los usuarios
        registrados en el sistema
        """
        relaciones = DBSession.query(Relaciones).all()
        lista =[]
        hijos =[]

        if id_item is not None:
            id_item=int(id_item)

        for rel in relaciones:
            for padre in rel.padres:
                if (padre.estado_oculto=="Activo"):
                    if padre.id_item == id_item:
                        lista.append(rel.id_item_hijo)
                        hijos.append (Item.get_item_by_id(rel.id_item_hijo) )                    
                        break

        while len(lista)>0:
            mis_hijos=Relaciones.get_mis_id_hijos(lista[0])
            del lista[0]
            for hijo in mis_hijos:
                if hijo not in lista:
                    item=Item.get_item_by_id(int(hijo))
                    if (padre.estado_oculto=="Activo"):
                        lista.append(hijo) 
                        hijos.append (item)

        return hijos

#-------------------------------------------------------------------------------

    @classmethod
    def get_padres_habilitados(self,orden):

        if orden is not None:
            orden=int(orden)

        padres=Item.get_item_activados()                                        #cambiar esta funcion y solo traer lo que no forman ciclos
        padres.remove(Item.get_master())

        fases_habilitadas=[]
        fases_habilitadas.append(orden)
        fases_habilitadas.append(orden-1)

        aux=[]
        for padre in padres:

            c=int(padre.orden)
            if  c not in fases_habilitadas or (padre.estado_oculto=="Activo"):
               aux.append(padre)

        for a in aux:
            padres.remove(a)       
        return padres

#-------------------------------------------------------------------------------

    @classmethod
    def matriz_relaciones(self,id_item):

        if id_item is not None:
            id_item=int(id_item)

        antecesores=Relaciones.get_antecesores(id_item)
        sucesores=Relaciones.get_sucesores(id_item)
        item=Item.get_item_by_id(id_item)
        relacionados=[]
        usados=[]

        n = len(antecesores)+len(sucesores)+1
        for antecesor in antecesores:
            if antecesor not in relacionados:
                if (antecesor.estado_oculto=="Activo"):
                    relacionados.append(antecesor)
                    usados.append(antecesor.nombre_item)

        if item not in relacionados:
            relacionados.append(item)
            usados.append(item.nombre_item)

        for sucesor in sucesores:
            if sucesor not in relacionados:
                if (sucesor.estado_oculto=="Activo"):
                    relacionados.append(sucesor)
                    usados.append(sucesor.nombre_item)
        #Graph creation
        gr = graph()

        # Add nodes and edges
        for item in usados:
            gr.add_nodes([item])
        
        # Add relation and edges

        for item in relacionados:
            padres= Relaciones.get_mis_padres(item.id_item)
            if len(padres)>0:
                for padre in padres:
                    gr.add_edge((item.nombre_item, padre.nombre_item))
            else:
                #remover nodo   
                print("hola") 
        

        # Draw as PNG
        dot = write(gr)
        gvv = gv.readstring(dot)
        gv.layout(gvv,'dot')
        gv.render(gvv,'png','/home/hermann/saip2011/saip2011/public/images/arbol.png')
    
        
#-------------------------------------------------------------------------------

    @classmethod
    def borrar_by_id(self,rel_id):
        """
        Obtiene la lista de todos los adjuntos         
        """
        DBSession.delete(DBSession.query(Relaciones).get(rel_id))
        DBSession.flush()	

#-------------------------------------------------------------------------------


