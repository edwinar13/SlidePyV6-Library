from slidepyv6 import SlideProject

# Create a new project
project = SlideProject("example_project.slim")

# Imprimir metadatos del proyecto 

# Titulo de la tabla
print("-" * 100)
print(f'{"Metadatos del proyecto":^10}')
print("-" * 100)

# Encabezados
print(f'{"Propiedad":<45}{"Valor":<45}')
print("-" * 100)

# Valores
print(f'{"Versión":<45}{project.metadata.version:<45}')
print(f'{"Título":<45}{project.metadata.title:<45}')
print(f'{"Análisis":<45}{project.metadata.analysis:<45}')
print(f'{"Autor":<45}{project.metadata.author:<45}')
print(f'{"Fecha":<45}{project.metadata.date:<45}')
print(f'{"Compañía":<45}{project.metadata.company:<45}')
print(f'{"Comentarios":<45}{str(project.metadata.comments):<45}')
print(f'{"Unidades":<45}{project.metadata.units:<45}')
print(f'{"Unidades de tiempo":<45}{project.metadata.time_units:<45}')
print(f'{"Unidades de permeabilidad imperial":<45}{project.metadata.permeability_units_imperial:<45}')
print(f'{"Unidades de permeabilidad métrico":<45}{project.metadata.permeability_units_metric:<45}')
print(f'{"Dirección":<45}{project.metadata.direction:<45}')
print(f'{"Número de materiales":<45}{project.metadata.nummaterials:<45}')
print(f'{"Número de anclajes":<45}{project.metadata.numanchors:<45}')
print(f'{"Valor de sismo horizontal":<45}{project.metadata.seismic:<45}')
print(f'{"Valor de sismo vertical":<45}{project.metadata.seismicv:<45}')
print("-" * 100)


