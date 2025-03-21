# src/slidepyv6/exceptions.py
from typing import Optional

class SlideError(Exception):
    """Base exception para todos los errores de la biblioteca"""
    def __init__(self, message: str = "Error en SlidePyV6", original_error: Exception = None):
        self.message = message
        self.original_error = original_error
        super().__init__(self.message)
    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"
    '''
    
    def __str__(self):
        if self.original_error:
            return f"{super().__str__()}\nCausa original: {type(self.original_error).__name__}: {str(self.original_error)}"
        return super().__str__()
    '''
    
    
# #############       validado ok      ################
class SlideFileError(SlideError):
    """Error relacionado con el manejo de archivos"""
    def __init__(self, message: str = "Error en archivo del proyecto"):
        super().__init__(message)
        self.error_code = 1001

class SlideTempDirectoryError(SlideError):
    """Error en la creación/gestión de directorios temporales"""
    def __init__(self, message: str = "Error en directorio temporal"):
        super().__init__(message)
        self.error_code = 1002

class SlideParsingError(SlideError):
    """Error en el parseo de archivos del proyecto"""
    def __init__(self, message: str = "Error parsing archivo"):
        super().__init__(message)
        self.error_code = 1003
        self.line_number: Optional[int] = None
        self.raw_content: Optional[str] = None

    def add_context(self, line: int = None, content: str = None) -> None:
        self.line_number = line
        self.raw_content = content
        self.message += f"\nContexto - Línea: {line}, Contenido: {content[:50]}" if content else ""