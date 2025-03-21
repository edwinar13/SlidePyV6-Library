from dataclasses import dataclass
from .geometries import Point


#####################################
#       clase secundaria
#####################################

@dataclass
class Method:
    id: int
    name: str

@dataclass
class Surface:
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
    resisting_moment: float | None
    driving_moment: float | None
    resisting_force: float | None
    driving_force: float | None

@dataclass
class GlobalMinimum:
    surface: Surface
    equilibrium_terms: EquilibriumTerms
    # Falta este campo
    #slices: list[Slice]


#####################################
#       clase principal
#####################################
@dataclass
class ProjectResults:
    methods: list[Method]
    surfaces: list[Surface]
    global_minimums: list[GlobalMinimum]




