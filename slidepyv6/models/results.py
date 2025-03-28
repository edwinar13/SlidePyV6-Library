from dataclasses import dataclass
from .geometries import Point


#####################################
#       clase secundaria
#####################################

@dataclass
class Method:
    """
    Clase Method que representa un método de estabilidad.
    Atributos:
    ----------
        id (int): Identificador único del método.
        name (str): Nombre del método.        
    """
    id: int
    name: str

@dataclass
class Surface:
    """
    Clase Surface que representa una superficie de falla.
    Atributos:
    ----------
        method (str): Método de estabilidad.
        radius (float): Radio de la superficie.
        point1 (Point): Primer punto de la superficie.
        point2 (Point): Segundo punto de la superficie.
        yleft (float): Coordenada y del punto izquierdo.
        yright (float): Coordenada y del punto derecho.
        fs (float): Factor de seguridad.
        point_center (Point): Punto central de la superficie.
        b1 (float): Parámetro b1.
    """
    method: str
    radius: float 
    point1: Point
    point2: Point
    yleft: float | None
    yright: float  | None
    fs: float
    point_center: Point
    b1: float | None


@dataclass
class Slice:
    """
    Clase Slice que representa un rebanada.
    Atributos:
    ----------
        x: float
        yt: float
        yb: float
        loc: int
        frictional_strength: float
        cohesive_strength: float
        base_normal_force: float
        base_friction_angle: float
        interslice_normal_force: float
        interslice_shear_force: float
        slice_weight: float
        pore_pressure: float
        m_alpha: float
        thrust_line_elevation: float
        initial_pore_pressure: float
        horizontal_seismic_force: float
        vertical_seismic_force: float
        phib: float
        base_cohesion: float
        base_material: str
    """
    x: float
    yt: float
    yb: float
    loc: int
    frictional_strength: float
    cohesive_strength: float
    base_normal_force: float
    base_friction_angle: float
    interslice_normal_force: float
    interslice_shear_force: float
    slice_weight: float
    pore_pressure: float
    m_alpha: float
    thrust_line_elevation: float
    initial_pore_pressure: float
    horizontal_seismic_force: float
    vertical_seismic_force: float
    phib: float
    base_cohesion: float
    base_material: str

@dataclass
class EquilibriumTerms:
    """
    Clase EquilibriumTerms que representa los términos de equilibrio.
    Atributos:
    ----------
        resisting_moment: float
        driving_moment: float
        resisting_force: float
        driving_force: float
    """
    resisting_moment: float | None
    driving_moment: float | None
    resisting_force: float | None
    driving_force: float | None

@dataclass
class GlobalMinimum:
    """
    Clase GlobalMinimum que representa un mínimo global.
    Atributos:
    ----------
        surface: Surface
        equilibrium_terms: EquilibriumTerms
        slices: list[Slice] (Falta este campo, para la versión 0.2.0)
    """
    surface: Surface
    equilibrium_terms: EquilibriumTerms
    # Falta este campo
    #slices: list[Slice]


#####################################
#       clase principal
#####################################
@dataclass
class ProjectResults:
    """
    Clase ProjectResults que representa los resultados de un proyecto.
    Atributos:
    ----------
        methods: list[Method]
        surfaces: list[Surface]
        global_minimums: list[GlobalMinimum]
    """
    methods: list[Method]
    surfaces: list[Surface]
    global_minimums: list[GlobalMinimum]




