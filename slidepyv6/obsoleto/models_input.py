from dataclasses import dataclass
from typing import List

@dataclass
class GeometryPoint:
    x: float
    y: float
    z: float = 0.0


#####################################
#       Soil Parameters
#####################################



@dataclass
class Vertice:
    num_vertice: int
    x: float
    y: float

@dataclass
class Cell:
    num_cell: int
    vertices: List[int]
    material: str

@dataclass
class Anchor:
    num_anchor_: str
    x1: float
    y1: float
    x2: float
    y2: float
    material: str

@dataclass
class Force:
     # 1 type: 0
     # x1: 5.881 y1: 7.994 x2: 2.71463476969864 y2: 7.994
     # angle: 270 load: 100 load2: 100
     # stage2: 0 design_standard_option: 0
    num_force: int
    force_type: int
    x1: float
    y1: float
    x2: float
    y2: float
    angle: float
    load: float
    load2: float



@dataclass
class Geometry:
    vertices: List[Vertice]
    cells: List[Cell]
    anchors: List[Anchor]
    water_table: List[float]
    slope: List[int]
    exterior: List[int]    
    forces: List[Force]
    slope_limits: tuple[GeometryPoint, GeometryPoint]|None

#####################################
#       Soil and Support Style
#####################################

@dataclass
class Color:
    red: int
    green: int
    blue: int

@dataclass
class SupportStyle:
    color: Color

@dataclass
class SoilStyle(SupportStyle):
    hatch: str | None

#####################################
#       Anchor Parameters
#####################################
#clase base anchor
@dataclass
class AnchorParameter:
    anchor_name: str
    anchor_style: SupportStyle
    anchor_number: str
    anchor_type_number: int
    '''
    application_force: float
    spacing: float
    capacity: float
    '''

@dataclass
class AnchorParameterEndAnchored(AnchorParameter):
    anchor_type: str = 'End Anchored'

@dataclass
class AnchorParameterGeoTextile(AnchorParameter):
    anchor_type: str = 'Geo-Textile'

@dataclass
class AnchorParameterGroutedTieback(AnchorParameter):
    anchor_type: str = 'Grouted Tieback'


@dataclass
class AnchorParameterGroutedTiebackFriction(AnchorParameter):
    anchor_type: str = 'Grouted Tieback Friction'

@dataclass
class AnchorParameterMicroPile(AnchorParameter):
    anchor_type: str = 'Micro Pile'

@dataclass
class AnchorParameterSoilNail(AnchorParameter):
    anchor_type: str = 'Soil Nail'









    


#####################################
#       Soil Parameters
#####################################

@dataclass
class SoilParameterMohrCoulomb:    
    soil_name: str
    soil_style: SoilStyle
    soil_number: str
    soil_type_number: int
    unit_weight: float
    satured_unit_weight: float | None

    cohesion: float
    friction_angle: float
    soil_type: str = 'Mohr Coulomb'
    '''
    water_surface: float
    hu_value: float
    ru_value: float
    '''
 
@dataclass
class SoilParameterUndrained:
    soil_name: str
    soil_style: SoilStyle
    soil_number: str
    soil_type_number: int


    unit_weight: float
    satured_unit_weight: float | None

    
    cohesion: float
    soil_type: str = 'Undrained'
    '''
    cohesion_type: int
    '''

 
@dataclass
class SoilParameterNoStrength:
    soil_name: str
    soil_style: SoilStyle
    soil_number: str
    soil_type_number: int
    unit_weight: float
    satured_unit_weight: float | None
    soil_type: str = 'No Strength'

@dataclass
class SoilParameterInfiniteStrength(SoilParameterNoStrength):
    pass
 

@dataclass
class SoilParameterHoekBrown:
    soil_name: str
    soil_style: SoilStyle
    soil_number: str
    soil_type_number: int


    unit_weight: float
    satured_unit_weight: float | None
    sigc: float
    mb: float
    s: float
    soil_type: str = 'Hoek Brown'
    '''
    water_surface: float
    hu_value: float
    ru_value: float
    '''
    
@dataclass
class SoilParameterGenHoekBrown(SoilParameterHoekBrown):
    a: float =0.0
    soil_type: str = 'General Hoek Brown'

'''
@dataclass
class SoilParameter:
    materialsMohrCoulomb: List[SoilParameterMohrCoulomb]
    materialsInfiniteStrength: List[SoilParameterInfiniteStrength]
'''



#####################################
#       General Settings
#####################################
@dataclass
class GeneralSettings:
    units: str
    time_units: str
    permeability_units_imperial: str
    permeability_units_metric: str
    direction: str
    nummaterials: int
    numanchors: int

@dataclass
class SeismicSettings:
    seismic: 0
    seismicv: 0  

@dataclass
class SummarySettings:
    title: str
    analysis: str
    author: str
    date: str
    company: str
    comments1: str
    comments2: str
    comments3: str
    comments4: str
    comments5: str
    
@dataclass
class ProjectSettings:
    general_settings: GeneralSettings
    summary_settings: SummarySettings
    seismic_settings: SeismicSettings




#####################################
# este es el modelo de datos principal
#####################################
@dataclass
class SlideInputData:
    # datos iniciales
    version: str
    project_settings: ProjectSettings | None
    soil_parameters: List[SoilParameterMohrCoulomb|SoilParameterUndrained|SoilParameterNoStrength|SoilParameterInfiniteStrength|SoilParameterHoekBrown|SoilParameterGenHoekBrown]
    anchor_parameters: List[AnchorParameterEndAnchored|AnchorParameterMicroPile]
    geometry: Geometry | None
