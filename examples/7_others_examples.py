from slidepyv6 import SlideProject

# Create a new project
project = SlideProject("example_project.slim")



# Métodos  ---------------------------------------------------------
min_fs = project.get_min_safety_factor()
print(f'{"→ FS mínimo de todos los métodos ="} {min_fs}')

critical = project.get_critical_surface()
print(f'{"→ Superficie crítica con menor FS ="} {critical}')








