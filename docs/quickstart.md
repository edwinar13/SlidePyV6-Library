# Guía de inicio rápido  
Esta es una guía de inicio rápido que le ayudará a comenzar a utilizar la aplicación `PySlideV6` en su proyecto de Python.  

## 🧑🏽‍💻 Cargar un proyecto  
Para cargar un proyecto de Slide V6, se debe crear un objeto de la clase `SlideProject`, pasando como argumento el archivo `.slim` que se desea cargar.  

```python
from slidepyv6 import SlideProject

proyecto = SlideProject("mi_proyecto.slim")
```

> **Nota:** Asegúrese de que el archivo `mi_proyecto.slim` se encuentra en la misma carpeta que el script de Python.

**`proyecto`** es un objeto de la clase `SlideProject` que representa el archivo `mi_proyecto.slim`. Este objeto  
contiene toda la información del proyecto, la cual se puede acceder mediante sus atributos y métodos.  

## Atributos  
Los atributos de un objeto `SlideProject` permiten acceder a los datos del proyecto de forma estructurada.  

##### **Notas:**  
- Los atributos son de solo lectura, es decir, no se pueden modificar.  
- **(Para versión 0.2.0)** Puedes obtener un diccionario de cada atributo utilizando el método `as_dict()`.  
  - Ejemplo: `proyecto.metadata.as_dict()`  


### Acceder a metadatos  
Los metadatos permiten obtener información general del proyecto, como la versión, el autor, la fecha de creación, entre otros.  

```python
metadatos = proyecto.metadata
```

El ejemplo de [metadatos](../examples/2_metadata_example.py) muestra cómo acceder a los metadatos de un proyecto de forma básica.  

### Acceder a propiedades  
Tanto los materiales como los soportes presentan propiedades que definen su comportamiento en el proyecto.  

```python
propiedades = proyecto.properties
```

El atributo `properties` devuelve un listado de las propiedades de materiales y soportes, las cuales pueden ser accedidas mediante los atributos `materials` y `supports`, como se muestra en el ejemplo de [propiedades](../examples/3_properties_example.py).  

### Acceder a geometría  
La geometría de un proyecto se compone principalmente de vértices, los cuales definen las celdas que conforman los diferentes materiales del proyecto. Estos vértices sirven para definir el contorno exterior del modelo, la pendiente superior, el nivel de agua, entre otros elementos.  

Además, la geometría también contiene los límites de análisis y los soportes.  

```python
geometria = proyecto.geometry
```

Para acceder a la geometría de un proyecto, se debe utilizar el atributo `geometry` del objeto `SlideProject`. Este atributo contiene información sobre los vértices, celdas, límites de análisis y soportes del proyecto. Estos pueden ser accedidos mediante los atributos `vertex`, `cells`, `exterior`, `slope`, `limits`, `water_table_vertex` y `supports`.  

El ejemplo de [geometría](../examples/4_geometry_example.py) muestra cómo acceder a la geometría de un proyecto de forma básica.  

### Acceder a cargas  
Las cargas de un proyecto pueden ser de dos tipos: lineales y distribuidas.  

```python
cargas = proyecto.loads
```

Para acceder a las cargas de un proyecto, se debe utilizar el atributo `loads` del objeto `SlideProject`. Este atributo contiene información sobre las cargas lineales y distribuidas, las cuales pueden ser accedidas mediante los atributos `linear` y `distributed`.  

El ejemplo de [cargas](../examples/5_loads_example.py) muestra cómo acceder a las cargas de un proyecto de forma básica.  

### Acceder a resultados  
Los resultados de un proyecto incluyen los métodos de análisis, los factores de seguridad y las superficies de falla.  

```python
resultados = proyecto.results
```

Para acceder a los resultados de un proyecto, se debe utilizar el atributo `results` del objeto `SlideProject`. Este atributo contiene información sobre los métodos de análisis, los factores de seguridad y las superficies de falla, los cuales pueden ser accedidos mediante los atributos `methods`, `surfaces` y `global_minimums`.  

El ejemplo de [resultados](../examples/6_results_example.py) muestra cómo acceder a los resultados de un proyecto de forma básica.  

## Métodos  
Los métodos de un objeto `SlideProject` permiten realizar operaciones y/o consultas específicas sobre el proyecto.  

### Calcular factor de seguridad mínimo  
```python
fs_min = proyecto.get_min_safety_factor()
```

### Analizar superficie crítica  
```python
superficie_critica = proyecto.get_critical_surface()
