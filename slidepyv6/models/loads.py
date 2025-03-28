from dataclasses import dataclass
from typing import List
from .geometries import Point

#####################################
#       clase base
#####################################

'''
carga dristribuida
['1', 'type:', '0', 'x1:', '6', 'y1:', '15', 'x2:', '3', 'y2:', '15', 'angle:', '270', 'load:', '100', 'load2:', '100', 'stage2:', '0', 'design_standard_option:', '0']
carga lineal
['3', 'type:', '1', 'x1:', '14', 'y1:', '15',                           'angle:', '270', 'load:', '30',                 'stage2:', '0', 'design_standard_option:', '0']
'''

@dataclass
class Load:
    """
    Representa una carga.

    Atributos:
    ----------
        point (Point): El punto de la carga.
        magnitude (float): La magnitud de la carga.
    """

    point: Point
    magnitude: float

@dataclass
class LinearLoad():
    """
    Representa una carga lineal aplicada.

    Atributos:
    ----------
        id (int): Identificador único para la carga.
        type_load (int): El tipo de carga (por ejemplo, puntuales, distribuidas, etc.).
        angle (float): El ángulo en el que se aplica la carga.
        load (Load): Carga principal.
        
    """
    id: int
    type_load: int
    angle: float
    load: Load


@dataclass
class DistributedLoad():
    """
    Representa una carga distribuida aplicada.

    Atributos:
    ----------
        id (int): Identificador único para la carga.
        type_load (int): El tipo de carga (por ejemplo, puntuales, distribuidas, etc.).
        angle (float): El ángulo en el que se aplica la carga.
        load (float): Carga principal.
        load2 (float): Carga secundaria.
    """
    id: int
    type_load: int
    angle: float
    load: Load
    load2: Load




@dataclass
class ProjectLoads:
    """
    Clase para almacenar las cargas aplicadas al modelo.

    Atributos:
    ----------
        linear (List[LinearLoad]): Lista de cargas lineales.
        distributed (List[DistributedLoad]): Lista de cargas distribuidas.
    """
    linear: List[LinearLoad]
    distributed: List[DistributedLoad]