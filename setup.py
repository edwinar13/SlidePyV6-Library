from setuptools import setup, find_packages

setup(
    name="slidepyv6",  # Nombre de tu biblioteca
    version="0.0.1",
    packages=find_packages(),  # Detecta automáticamente los paquetes dentro del proyecto
    install_requires=[],  # Dependencias (vacío si no hay)
)


'''
import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.1' #Muy importante, deberéis ir cambiando la versión de vuestra librería según incluyáis nuevas funcionalidades
PACKAGE_NAME = 'Leer_PDF' #Debe coincidir con el nombre de la carpeta 
AUTHOR = 'Antonio Fernandez Troyano' #Modificar con vuestros datos
AUTHOR_EMAIL = 'a.fernandez.troyano@gmail.com' #Modificar con vuestros datos
URL = 'https://github.com/afernandez119' #Modificar con vuestros datos

LICENSE = 'MIT' #Tipo de licencia
DESCRIPTION = 'Librería para leer ficheros PDFs y extraer la información en formato str' #Descripción corta
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8') #Referencia al documento README con una descripción más elaborada
LONG_DESC_TYPE = "text/markdown"


#Paquetes necesarios para que funcione la libreía. Se instalarán a la vez si no lo tuvieras ya instalado
INSTALL_REQUIRES = [
      'pymupdf'
      ]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)
'''