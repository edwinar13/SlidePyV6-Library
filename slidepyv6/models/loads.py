from dataclasses import dataclass
from typing import List
from .geometries import Point

#####################################
#       clase base
#####################################

@dataclass
class Force:
    """
    Representa una fuerza aplicada.

    Atributos:
    ----------
        id (int): Identificador único para la fuerza.
        point1 (Point): El punto de inicio de la fuerza.
        point2 (Point): El punto final de la fuerza.
        angle (float): El ángulo en el que se aplica la fuerza.
        type_load (int): El tipo de carga (por ejemplo, puntuales, distribuidas, etc.).
        load (float): La magnitud de la carga principal.
        load2 (float | None): La magnitud de la carga secundaria, si aplica.
    """
    id: int
    point1: Point
    point2: Point
    angle: float
    type_load: int
    load: float
    load2: float | None

@dataclass
class ProjectLoads:
    """
    Clase para almacenar las cargas aplicadas al modelo.

    Atributos:
    ----------
        forces (List[Force]): Lista de fuerzas aplicadas al modelo.
    """
    forces: List[Force]