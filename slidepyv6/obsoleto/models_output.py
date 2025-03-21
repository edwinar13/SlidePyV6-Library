from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple

########################################################
# estos son los modelos para los FS de los minimos
########################################################

# estos son los modelos basiccos
@dataclass
class SliceData:
    x: float # x coordinate
    yt: float  # top y coordinate
    yb: float  # bottom y coordinate
    loc: int 



# estos son los modelos para los sub-datos
@dataclass
class MinimumSurfaceInfo:
    slices: List[SliceData]
    method_name: str



@dataclass
class AnalysisResults:
    nun_results: int
    # For moment equilibrium methods (Bishop, Spencer)
    resisting_moment: Optional[float] = None
    driving_moment: Optional[float] = None    
    # For force equilibrium methods (Janbu, Spencer) 
    resisting_force: Optional[float] = None
    driving_force: Optional[float] = None
    
@dataclass
class GlobalMinimum:
    xc: float  # center x
    yc: float  # center y
    r: float   # radius
    x1: float  # start x
    y1: float  # start y
    x2: float  # end x
    y2: float  # end y
    fs: float  # factor of safety
    method: str  # analysis method name


########################################################
# estos son los modelos para los datos de la grilla
########################################################
@dataclass
class Surface:
    r: float # radius
    yleft: float # left y coordinate
    x1: float # start x
    y1: float # start y
    x2: float # end x
    y2: float # end y
    yright: float # right y coordinate
    fs: List[float] # factor of safety
    b1: float 
    xc: float | None
    yc: float | None

@dataclass
class Point:
    xc: float
    yc: float
    nun_surfaces: int
    surfaces: List[Surface]

@dataclass
class Grid:
    nun_grid: int
    nx: int
    ny: int    
    points: List[Point]

#####################################
# este es el modelo de datos principal
#####################################
@dataclass
class SlideOutputData:
    # datos iniciales
    version: str

    # grillas # → grids
    nun_grids: int 

    # tipos de analisis # → analysis
    nun_analysis_types: int 
    analysis_names: List[str]

    # superfies de falla # → surfaces
    surfaces: List[Surface]
    grids_results_fs: List[Grid]
    global_minimums_fs: List[GlobalMinimum]


    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
    # En Desarrollo
    # Resultados especificos de los minimos en cada metodo
    analysis_results: List[AnalysisResults]
    minimum_surfaces: List[MinimumSurfaceInfo]
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
    # aca falta la aprte de reusltados de las dobelas 
    # desde aca '* #data' hasta el final

   
