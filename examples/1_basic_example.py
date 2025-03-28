from slidepyv6 import SlideProject

# Create a new project
project = SlideProject("example_project.slim")


print(f'Objeto: {project}')
print(f'Tipo: {type(project)}')
print(f'Se ha ejecuta el análisis de estabilidad: {project.has_results()}')
