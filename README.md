# SlidePyV6: Biblioteca para manipulación de archivos .slim de Slide V6 (Rocscience)

> Una biblioteca de Python para leer y manipular análisis de estabilidad de equilibrio límite en proyectos con Slide V6 de Rocscience (archivos .slim), proporcionando acceso estructurado a geometrías, propiedades, cargas y resultados.
>

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Licencia](https://img.shields.io/badge/Licencia-MIT-green)

## Características principales
- **Lectura de proyectos**: Carga todos los componentes de un archivo .slim.
- **Modelado de datos**: Estructuras tipo `dataclass` para:
  - Metadatos del proyecto.
  - Propiedades de materiales (Mohr-Coulomb, Hoek-Brown, etc.).
  - Geometría (vértices, celdas, soportes).
  - Cargas y fuerzas.
  - Resultados de análisis (superficies críticas, factores de seguridad).
- **Extracción de resultados**: Factor de seguridad mínimo, superficie crítica.
- **Validación integrada**: Verificación de integridad de archivos.

-----------------------

# Uso básico

### Instalación
```bash
pip install slidepyv6
```

### Cargar un proyecto
```python
from slidepyv6 import SlideProject
proyecto = SlideProject("mi_proyecto.slim")
```

### Acceder a metadatos
```python
print(f"Versión: {proyecto.metadata.version}")
print(f"Autor: {proyecto.metadata.author}")
```

-----------------------

# Ejemplo avanzado
Para ver ejemplos avanzados, consulta la [guía de inicio rápido](./docs/quickstart.md) para obtener detalles técnicos.

-----------------------

# Estructura del proyecto
Un proyecto de Slide V6 (.slim) se compone de varios elementos, cada uno representado por una clase en SlidePyV6. 
Las clases reflejan parte del contenido de un archivo .slim y permiten acceder a los datos de forma estructurada.

### Clases principales:
- `SlideProject`: Punto de entrada principal.
  - `ProjectMetadata`: Metadatos del proyecto.
  - `ProjectProperties`: Propiedades de materiales y soportes.
  - `ProjectGeometry`: Geometría completa del modelo.
  - `ProjectLoads`: Cargas y fuerzas aplicadas.
  - `ProjectResults`: Resultados del análisis.

-----------------------

# Dependencias
- Python 3.9+
- Bibliotecas estándar:
    - `zipfile`
    - `pathlib`
    - `dataclasses`
    - `logging`
    - `typing`
    - `tempfile`
    - `shutil`
    - `re`
- Bibliotecas externas: No requiere instalación adicional.

-----------------------

# Contribución

## 🛠️ Codificando
Si deseas contribuir al desarrollo de SlidePyV6, consulta la [guía para desarrolladores](./docs/developer.md) para obtener detalles técnicos.

## 💰 Donando
Si este proyecto te ha sido útil, considera hacer una donación para apoyar su desarrollo continuo.

[![Invítame a un café](https://img.shields.io/badge/Buy_me_a_coffee-donate-orange.svg)](https://buymeacoffee.com/edwinarevau)

-----------------------

## 📬 Contacto
¿Dudas técnicas o colaboraciones? Escríbeme a:
- **Email**: [terrioingeniera@gmail.com](mailto:terrioingeniera@gmail.com)
- **LinkedIn**: [Edwin Arévalo](https://www.linkedin.com/in/edwin-j-arevalo/)

-----------------------

# Licencia
Distribuido bajo licencia MIT. Consulta el archivo [LICENSE](./LICENSE.txt) para más detalles.

-----------------------

## 🆘 Soporte  
¿Encontraste un error o tienes una idea?  
- Abre un **[issue](https://github.com/edwinar13/SlidePyV6-Library/issues)** en GitHub.  
- ¿Necesitas ayuda rápida? Etiqueta tu issue como `[Urgente]`.  

> ⚠️ **Importante**: Antes de reportar, verifica si ya existe un issue relacionado.
