from dataclasses import dataclass

#####################################
#       clase principal
#####################################

@dataclass
class ProjectMetadata:
    """
    Clase para almacenar la metadata del proyecto.

    Attributes:
    ----------
        version (str): Versión del proyecto.
        title (str): Título del proyecto.
        analysis (str): Tipo de análisis realizado.
        author (str): Autor del proyecto.
        date (str): Fecha del proyecto.
        company (str): Compañía responsable del proyecto.
        comments (list[str]): Comentarios adicionales sobre el proyecto.

        units (str): Unidades generales utilizadas en el proyecto.
        time_units (str): Unidades de tiempo utilizadas en el proyecto.
        permeability_units_imperial (str): Unidades de permeabilidad en sistema imperial.
        permeability_units_metric (str): Unidades de permeabilidad en sistema métrico.
        direction (str): Dirección del análisis.
        nummaterials (int): Número de materiales utilizados en el proyecto.
        numanchors (int): Número de anclajes utilizados en el proyecto.

        seismic (float): Valor de sismo horizontal.
        seismicv (float): Valor de sismo vertical.
    """

    # Summary
    version: str
    title: str
    analysis: str
    author: str
    date: str
    company: str
    comments: list[str]

    # General
    units: str
    time_units: str
    permeability_units_imperial: str
    permeability_units_metric: str
    direction: str
    nummaterials: int
    numanchors: int

    # Seismic
    seismic: float
    seismicv: float