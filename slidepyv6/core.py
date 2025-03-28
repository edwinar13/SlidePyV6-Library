#  imports
from .io.io import SlideProjectIO
from .utils.exceptions import SlideError
from .models.metadata import ProjectMetadata
from .models.properties import ProjectProperties
from .models.geometries import ProjectGeometry
from .models.loads import ProjectLoads
from .models.results import ProjectResults
from pathlib import Path
import logging

# logging
logger = logging.getLogger(__name__)

class SlideProject:
    
    def __init__(self, project_path: str):
        """
        Clase principal que representa un proyecto de Slide V6
        
        Args:
            project_path: Ruta al archivo .slim original
        """
        logger.debug("Inicializando proyecto: %s", project_path)
        self._io = SlideProjectIO(Path(project_path))


    def __del__(self):
        """Destructor que asegura la limpieza de recursos"""        
        self._io.cleanup()

    # Metadatos  -------------------------------------------------    
    @property       
    def metadata(self) -> ProjectMetadata:
        """ Obtiene la metadata del proyecto"""
        return self._io.metadata

    # Propiedades -------------------------------------------------    
    @property
    def properties(self) -> ProjectProperties:
        """Diccionario con propiedades clave"""
        return  self._io.properties
   
    # Geometria -------------------------------------------------    
    @property
    def geometry(self) -> ProjectGeometry:
        """Diccionario con geometria clave"""        
        return self._io.geometry

    # Cargas -------------------------------------------------    
    @property
    def loads(self) -> ProjectLoads:
        """Obtiene la lista de cargas"""
        return self._io.loads
   
    # Resultados -------------------------------------------------    
    @property
    def results(self) -> ProjectResults:
        """Obtiene la lista de resultados"""
        if not self._io.get_has_results():
            raise SlideError("El proyecto no tiene resultados, ejecute el analisis en Slide")
        return self._io.results


    # Métodos  ---------------------------------------------------------

    # Obtiene el FS mínimo de todos los métodos
    def get_min_safety_factor(self) -> float:
        """Obtiene el FS mínimo de todos los métodos"""
        if not self._io.get_has_results():
            raise SlideError("El proyecto no tiene resultados")
        return min(min.surface.fs for min in self._io.results.global_minimums)

    # Obtiene la superficie crítica con menor FS
    def get_critical_surface(self) -> dict:
        """Obtiene la superficie crítica con menor FS"""
        if not self._io.get_has_results():
            raise SlideError("El proyecto no tiene resultados")
        
        min_fs = self.get_min_safety_factor()
        critical = next(
            (m for m in self._io.results.global_minimums if m.surface.fs == min_fs), 
            None
        )
        surface_critical = critical.surface
        return {
            "center": (surface_critical.point_center.x, surface_critical.point_center.y),
            "radius": surface_critical.radius,
            "fs": surface_critical.fs,
            "method": surface_critical.method
        }

    # verifica si el proyecto ha sido ejecutado (tiene o no reusltados)
    def has_results(self) -> bool:
        """Verifica si el proyecto ha sido ejecutado"""
        return self._io.get_has_results()








'''
    ############################################################
    #         REVISAR ESTO PARA LECTURA DE PROYECTO
    ############################################################

    def has_results(self) -> bool:
        return self._io.get_has_results()
    
    def save(self, output_path: Union[str, Path], overwrite: bool = False) -> None:
        """Guarda el proyecto modificado"""
        if not self._is_modified:
            logger.info("No hay cambios para guardar")
            return
            
        try:
            self._io.save_project(output_path, overwrite)
            self._is_modified = False
        except Exception as e:
            raise SlideError(f"Error guardando proyecto: {e}") from e
        
    # para usar el SlideProject como un context manager    
    def __enter__(self):
        """Context manager para manejo seguro de recursos"""
        self.open()
        return self
    
    # para usar el SlideProject como un context manager
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Garantiza la limpieza al salir del contexto"""
        self.close()

    # para usar el SlideProject manualmente con try/finally
    def open(self) -> None:
        """Carga el proyecto en memoria"""
  
        try:
            self._io.decompress_project()
            self._parse_project()
        except Exception as e:
            self._io.cleanup()
            raise SlideError(f"Error abriendo proyecto: {e}") from e
    
    # para usar el SlideProject manualmente con try/finally
    def close(self) -> None:
        """Libera recursos y limpia temporales"""
        self._io.cleanup()        
        self._is_modified = False    
    
'''