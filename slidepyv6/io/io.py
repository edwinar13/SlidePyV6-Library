from ..utils.exceptions import SlideFileError, SlideTempDirectoryError
from ..models.metadata import ProjectMetadata
from ..models.properties import ProjectProperties
from ..models.geometries import ProjectGeometry
from ..models.loads import ProjectLoads
from ..models.results import ProjectResults
from .parsers.input_parser import InputParser
from .parsers.output_parser import OutputParser
import zipfile
import tempfile
import shutil
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class SlideProjectIO:
    def __init__(self, project_path: Path):
        """
        Maneja la lectura/escritura segura de proyectos Slide V6
        
        Args:
            project_path: Ruta al archivo .slim original
        """
        self._original_path = project_path.absolute()      
        self._temp_dir = None
        self._parsed_data = {
            'metadata': None,
            'properties': None,
            'loads': None,
            'geometrys': None,
            'results': None
        }
        self.has_results = False
        self._full_parse()


    # ---------------------------------------------------------
    #                      Metodos Protegidos 
    # ---------------------------------------------------------
    def _full_parse(self):
        """Realiza la validación y parseo completo del proyecto"""

        try:
            # *****************************************************
            self._validate_input_file()
            self._decompress_project()
            self._parse_files()
            
            '''
            # esto es temporal para debug
            self.inputContentSave()
            self.outputContentSave()

            '''
            # *****************************************************
        except Exception as e:
            self.cleanup()
            raise SlideFileError(f"Error al validar el archivo de entrada: {e}") from e
        finally:
            self.cleanup()
    

    def _validate_input_file(self) -> None:
        """Verifica que el archivo de entrada sea válido"""
        if not self._original_path.exists():
            raise SlideFileError(f"Archivo no encontrado: {self._original_path}")
            
        if self._original_path.suffix.lower() != '.slim':
            raise SlideFileError("Extensión de archivo inválida. Debe ser .slim")

    def _decompress_project(self) -> Path:
        """
        Descomprime el proyecto .slim al directorio temporal

        Devuelve:
        ----------
            Path: Ruta al directorio temporal con los archivos descomprimidos
        """
        if not self._temp_dir:
            self._create_temp_dir()

        try:
            with zipfile.ZipFile(self._original_path, 'r') as zip_ref:
                zip_ref.extractall(self._temp_dir)
                
            self._verify_decompressed_files()
            return self._temp_dir
            
        except zipfile.BadZipFile as e:
            raise SlideFileError("Archivo .slim corrupto o inválido") from e
        except Exception as e:
            raise SlideFileError(f"Error descomprimiendo archivo: {e}") from e

    def _create_temp_dir(self) -> Path:
        """
        Crea un directorio temporal único y seguro para trabajar

        Devuelve:
        ----------
            Path: Ruta al directorio temporal creado
        """
        if self._temp_dir and self._temp_dir.exists():
            self.cleanup()
            
        try:
            # Usamos tempfile para mejor manejo de permisos y seguridad
            temp_dir = tempfile.mkdtemp(prefix="slidepyv6_")
            self._temp_dir = Path(temp_dir)
            logger.debug(f"Directorio temporal creado: {self._temp_dir}")
            return self._temp_dir
        except OSError as e:
            raise SlideTempDirectoryError(f"Error creando directorio temporal: {e}")

    def _verify_decompressed_files(self) -> None:
        """Verifica la presencia de archivos esenciales"""
        #-------------------------------------------
        # los archivos de un .slim sin analisis son:
        # .sli: Configuración principal *
        # .slv: Slide View Options File *
        #-------------------------------------------
        # los archivos de un .slim con analisis son:
        # .emf: parece un archivo binario
        # .s01: Resultados
        # .sli: Configuración principal *
        # .sltm: Slide Tools File
        # .slv: Slide View Options File *
        # .slvi: Slide Interpret View States Filee *
        #------------------------------------------- 
        # los archivos con * son los mismos para ambos 
        # tipos de proyectos
        #-------------------------------------------

        required_files = {
            '.sli',  # requerido (escritura)
            '.s01'   # requerido (lectura)
        } 
        existing_files = {f.suffix for f in self._temp_dir.glob('*')}
        missing = required_files - existing_files
        logging.debug(f"Archivos encontrados: {existing_files}, faltantes: {missing}")
        self.has_results = True


        if '.sli' not in existing_files:
            raise SlideFileError(
                f"Archivos esenciales faltantes en el proyecto: {', '.join(missing)}"
            )
        
        if '.s01' not in existing_files:
            self.has_results = False
            print(f"WARNING: No se encontró el archivo de resultados en el proyecto")
            print(f"WARNING: Las funcionalidades de lectura de resultados podran generar errores o comportamientos inesperados")            
           
            # Crear archivo de salida temporal en la carpeta temporal            
            name = "no_results"
            output_file = self._temp_dir / f"{name}.s01"
            output_file.touch()


    def _parse_files(self):
        """Parsea y carga todos los datos a memoria"""

        input_content = self._read_project_file('input')
        metadata, properties, geometries, loads = InputParser.parse(input_content)
        self._parsed_data['metadata'] = metadata
        self._parsed_data['properties'] = properties
        self._parsed_data['geometry'] = geometries
        self._parsed_data['loads'] = loads
        
        # Leer y parsear output si existe       
        if self.has_results:
            output_content = self._read_project_file('output')
            #if isinstance(output_content, bytes):
            #    output_content = output_content.decode('utf-8', errors='ignore')
            results = OutputParser.parse(output_content)

            self._parsed_data['results']  = results
        try:
            pass

        except Exception as e:
            self.cleanup()
            raise SlideFileError(f"Error parsing files: {e}") from e


    # ---------------------------------------------------------
    #                      Metodos Publicos 
    # ---------------------------------------------------------
    @property
    def metadata(self) -> ProjectMetadata:
        return self._parsed_data['metadata']
    
    @property
    def properties(self) -> ProjectProperties:    
        return self._parsed_data['properties']

    @property
    def geometry(self) -> ProjectGeometry:
        return self._parsed_data['geometry']
    

    @property
    def loads(self) -> ProjectLoads:
        return self._parsed_data['loads']
    
    @property
    def results(self) -> ProjectResults:
        return self._parsed_data['results']


    # ##################################################
    #           Otras funciones
    # ##################################################

    def _read_project_file(self, type_file: str) -> str:
        """
        Lee el contenido de un archivo del proyecto por su extensión
        
        Args:
            type_file: Tipo de archivo input => sli output => s01
            
        Devuelve:
            str: Contenido del archivo decodificado
        """
   
        if not self._temp_dir:
            raise SlideFileError("Proyecto no descomprimido")

        if type_file == 'input':
            suffix = '.sli'
        elif type_file == 'output':
            suffix = '.s01'
        else:
            raise SlideFileError(f"Tipo de archivo inválido: {type_file}")
            
        target_file = next(self._temp_dir.glob(f"*{suffix}"), None)
        
        if not target_file or not target_file.exists():
            raise SlideFileError(f"Archivo con extensión {suffix} no encontrado")
            
        try:
            # Asumimos que los archivos de texto usan UTF-8
            return target_file.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            # Fallback para archivos binarios como .emf
            return target_file.read_bytes()

    def cleanup(self) -> None:
        """Elimina de forma segura el directorio temporal"""
        
        if self._temp_dir and self._temp_dir.exists():
            try:
                shutil.rmtree(self._temp_dir)
                logger.debug(f"Directorio temporal eliminado: {self._temp_dir}")
            except Exception as e:
                logger.error(f"Error limpiando directorio temporal: {e}")
            finally:
                self._temp_dir = None

    def get_has_results(self) -> bool:
        return self.has_results

    # ##################################################
    #           METODOS TEMPORALES PARA DEBUG
    # ##################################################

    def outputContentSave(self):        
        output_content = self._read_project_file('output')  
        lines = output_content.splitlines()        
        # crear un archivo temporal
        with open('output.txt', 'w') as f:
            for line in lines:
                f.write(line + '\n')

    def inputContentSave(self):          
        input_content = self._read_project_file('input')
        if isinstance(input_content, bytes):
            input_content = input_content.decode('utf-8', errors='ignore')
        lines = input_content.splitlines()
        # crear un archivo temporal
        with open('input.txt', 'w') as f:
            for line in lines:
                f.write(line + '\n')
