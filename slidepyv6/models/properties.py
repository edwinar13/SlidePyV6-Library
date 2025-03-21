from dataclasses import dataclass
from typing import List, Union
#####################################
# --- Clases Base ---
#####################################

@dataclass(frozen=True)
class Color:
    """
    Clase que representa un color en el modelo RGB.

    Atributos:
    -----------
        red (int): Componente rojo del color (0-255).
        green (int): Componente verde del color (0-255).
        blue (int): Componente azul del color (0-255).
    """
    red: int
    green: int
    blue: int

@dataclass
class BaseProperty:
    """
    Clase BaseProperty que representa una propiedad base con un identificador, nombre y color.

    Atributos:
    -----------
        id (str): Identificador único de la propiedad.
        name (str): Nombre de la propiedad.
        color (Color): Color asociado a la propiedad.
    """
    id: str
    name: str
    color: Color


#####################################
# --- Materiales (Composición) ---
#####################################

@dataclass
class MohrCoulombParams:
    """
    Clase que representa los parámetros de un material de Mohr-Coulomb.

    Atributos:
    -----------
        cohesion (float): Cohesión del material.
        friction_angle (float): Ángulo de fricción del material.
    """
    cohesion: float
    friction_angle: float
    # Faltan parametros de agua
    # hu: float 
    # ru: float

@dataclass
class UndrainedParams:
    """
    Clase que representa los parámetros no drenados.

    Atributos:
    -----------
        cohesion (float): Cohesión del suelo.
        c_type (int): Tipo de cohesión.
    """
    cohesion: float
    c_type: int

@dataclass
class NoStrengthParams:
    """
    Clase que representa los parámetros de resistencia nula.

    Esta clase es un marcador de posición y actualmente no contiene atributos ni métodos.
    """
    pass

@dataclass  
class InfiniteStrengthParams:
    """
    Clase que representa los parámetros de resistencia infinita.

    Esta clase es un marcador de posición y actualmente no contiene atributos ni métodos.
    """
    pass

@dataclass
class HoekBrownParams:
    """
    Clase para almacenar los parámetros del criterio de rotura de Hoek-Brown.

    Atributos:
    -----------
        sigc (float): Resistencia a compresión uniaxial del material intacto.
        mb (float): Parámetro de Hoek-Brown que depende de la calidad del macizo rocoso.
        s (float): Parámetro de Hoek-Brown que depende de la condición del macizo rocoso.
    """
    sigc: float
    mb: float
    s: float

@dataclass
class GeneralHoekBrownParams:
    """
    Clase que representa los parámetros generales del criterio de falla de Hoek-Brown.

    Atributos:
    -----------
        sigc (float): Resistencia a la compresión uniaxial de la roca intacta.
        mb (float): Parámetro 'mb' del criterio de Hoek-Brown.
        s (float): Parámetro 's' del criterio de Hoek-Brown.
        a (float): Parámetro 'a' del criterio de Hoek-Brown.
    """
    sigc: float =0.0
    mb: float =0.0  
    s: float =0.0
    a: float =0.0

@dataclass
class PropertyMaterial(BaseProperty):
    """
    Clase PropertyMaterial que hereda de BaseProperty.

    Atributos:
    -----------
        hatch (str): Patrón de sombreado del material.
        unit_weight (float): Peso unitario del material.
        satured_unit_weight (float | None): Peso unitario saturado del material, puede ser None.
        material_params (Union[MohrCoulombParams, HoekBrownParams, GeneralHoekBrownParams, UndrainedParams, NoStrengthParams, InfiniteStrengthParams]): 
            Parámetros del material que pueden ser de diferentes tipos de modelos de resistencia.
    """
    hatch: str 
    unit_weight: float
    satured_unit_weight: float | None
    material_params: Union[MohrCoulombParams, HoekBrownParams, GeneralHoekBrownParams, UndrainedParams, NoStrengthParams, InfiniteStrengthParams]


#####################################
# --- Soportes (Composición) ---
#####################################

@dataclass
class EndAnchoredParams:
    """
    Clase para representar los parámetros de anclaje final.

    Atributos:
    -----------
        fa (int): Aplicación de fuerza.
        sp (float): Espaciado.
        cap (float): Capacidad.
    """
    fa: int # force aplication
    sp: float # spacing
    cap: float # capacity
    
@dataclass
class GeoTextileParams:
    """
    Clase que representa los parámetros de un geotextil.

    Atributos:
    -----------
        fa (int): Fuerza de aplicación.
        ts (float): Resistencia a la tracción.
        po_adh (float): Adhesión al arrancamiento.
        po_fric (float): Fricción al arrancamiento.
    """
    fa: int # force aplication
    ts: float # tensile strength
    po_adh: float # Pullout adhesion
    po_fric: float # Pullout friction

@dataclass
class GroutedTiebackParams:
    """
    Clase que representa los parámetros de un anclaje grouteado.

    Atributos:
    -----------
    fa (int):Fuerza de aplicación.
    sp (float):Espaciado.
    cap (float):Capacidad de tensión.
    pc (float):Capacidad de placa.
    bs (float):Resistencia al corte.
    bt (int):Tipo de anclaje 0→Longitud 1→Porcentaje.
    bl (float):Longitud de anclaje.
    """
    fa: int # force aplication
    sp: float # spacing
    cap: float # Tensile capacity
    pc: float # plate capacity
    bs: float # bond strength
    bt: int # bond type 0→Length 1→Pecent 
    bl: float # bond length

@dataclass
class GroutedTiebackFrictionParams:
    """
    Clase que representa los parámetros de un anclaje grouteado con fricción.

    Atributos:
    -----------
        fa (int):Fuerza de aplicación.
        sp (float):Espaciado.
        cap (float):Capacidad de tensión.
        pc (float):Capacidad de placa.
        bt (int):Tipo de anclaje 0→Longitud 1→Porcentaje.
        bl (float):Longitud de anclaje.
        po_adh (float):Adhesión al arrancamiento.
        po_fric (float):Fricción al arrancamiento.
    """
    fa: int # force aplication
    sp: float # spacing
    cap: float # Tensile capacity
    pc: float # plate capacity
    bt: int # bond type 0→Length 1→Pecent 
    bl: float # bond length
    po_adh: float # Pullout adhesion
    po_fric: float # Pullout friction

@dataclass
class MicroPileParams:
    """
    Clase que representa los parámetros de un micropilote.

    Atributos:
    -----------
        fa (int):Fuerza de aplicación.
        sp (float):Espaciado.
        mpss (float):Capacidad de tensión.
        mpforcedirection (int):Dirección de la fuerza.
    """
    fa: int
    sp: float
    mpss: float
    mpforcedirection : int

@dataclass
class SoilNailParams:
    """
    Clase que representa los parámetros de un anclaje de suelo.

    Atributos:
    -----------
        fa (int):Fuerza de aplicación.
        sp (float):Espaciado.
        cap (float):Capacidad de tensión.
        pc (float):Capacidad de placa.
        bs (float):Resistencia al corte.
    """
    fa: int
    sp: float 
    cap: float
    pc: float
    bs: float

@dataclass
class PropertySupport(BaseProperty):
    """
    Clase PropertySupport que hereda de BaseProperty representando un soporte.

    Atributos: 
    -----------     
        support_params (Union[EndAnchoredParams, GeoTextileParams, GroutedTiebackParams, GroutedTiebackFrictionParams, MicroPileParams, SoilNailParams]): 
            Parámetros del soporte que pueden ser de diferentes tipos de soportes.

    """
    support_params: Union[EndAnchoredParams, GeoTextileParams, GroutedTiebackParams, GroutedTiebackFrictionParams, MicroPileParams, SoilNailParams]

#####################################
#       clase principal
#####################################

@dataclass
class ProjectProperties:
    """
    Clase para almacenar las propiedades de los materiales y soportes.

    Atributos:
    ----------
        materials (List[PropertyMaterial]): Lista de materiales.
        supports (List[PropertySupport]): Lista de soportes.

    """
    materials: List[PropertyMaterial]
    supports: List[PropertySupport]
