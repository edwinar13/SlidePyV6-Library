from dataclasses import dataclass
from typing import List

#####################################
#       clase base
#####################################

@dataclass (frozen=True)
class Point:
    """
    Representa un punto en el espacio 2D.

    Atributos:
    ----------
        x (float): La coordenada x del punto.
        y (float): La coordenada y del punto.
    """
    x: float
    y: float

#####################################
#       clase secundaria
#####################################

@dataclass
class Vertex:
    """
    Clase Vertex que representa un vértice en una geometría.

    Atributos:
    ----------
        id (int): Identificador único del vértice.
        point (Point): Punto que define la posición del vértice.
    """
    id: int
    point: Point

@dataclass
class Cell:
    """
    Clase que representa una celda en una geometría asociada a un material.

    Atributos:
    ----------
        id (int): Identificador único de la celda.
        vertices (List[Vertex]): Lista de vértices que definen la celda.
        property_id (str): Referencia al identificador de la propiedad del material asociado a la celda.
    """
    id: int
    vertices: List[Vertex]
    property_id: str  # Referencia a property.materials

@dataclass
class Support:
    """
    Clase que representa un soporte en una geometría asociado a un soporte.

    Atributos:
    ----------
        id (int): Identificador único del soporte.
        point1 (Point): Primer punto que define el soporte.
        point2 (Point): Segundo punto que define el soporte.
        property_id (str): Referencia a la propiedad del soporte.
    """
    id: int
    point1: Point
    point2: Point
    property_id: str  # Referencia a property.support

#####################################
#       clase principal
#####################################

@dataclass
class ProjectGeometry:
    """
    Clase que representa la geometría de un proyecto.

    Atributos:
    ----------
        vertex (List[Vertex]): Lista de vértices que definen la geometría.
        cells (List[Cell]): Lista de celdas que definen la geometría.
        supports (List[Support]): Lista de soportes que definen la geometría.
        water_table_vertex (List[Vertex]): Lista de vértices que definen la tabla de agua.
        limits (tuple[Point, Point]|None): Límites de la geometría.
        slope (List[Vertex]): Lista de vértices que definen la pendiente de la geometría.
        exterior (List[Vertex]): Lista de vértices que definen el exterior de la geometría.
    """
    vertex: List[Vertex]
    cells: List[Cell]
    supports: List[Support]
    water_table_vertex: List[Vertex]    
    limits: tuple[Point, Point]|None
    slope: List[Vertex]
    exterior: List[Vertex]