from slidepyv6 import SlideProject

# Create a new project
project = SlideProject("example_project.slim")


# Resultados del proyecto
results  = project.results

# Métodos
methods = results.methods
print("-" * 30)
print(f'{"→ Métodos de análisis"}')
for method in results.methods:
    id = method.id
    name = method.name
    print(f'id: {id}, name: {name}')


# Superficies
surfaces = results.surfaces
print("-" * 30)
print(f'{"→ Superficies"}')
for surface in results.surfaces:
    method = surface.method
    fs = surface.fs
    pc = surface.point_center
    radius = surface.radius
    print(f'method: {method}, fs: {fs}, pc: {pc}, radius: {radius}')



# Factores de seguridad mínimos globales
global_minimums = results.global_minimums
print("-" * 30)
print(f'{"→ Factores de seguridad mínimos globales"}')
for global_minimum in results.global_minimums:
    
    surface = global_minimum.surface
    method = surface.method
    fs = surface.fs
    pc = surface.point_center
    radius = surface.radius    
    print(f'\n    Surface = method: {method}, fs: {fs}, pc: [{pc.x:0.3f}, {pc.y:0.3f}], radius: {radius}')  
    equilibrium_terms = global_minimum.equilibrium_terms
    print(f'    Equilibrium Terms = resisting_moment: {equilibrium_terms.resisting_moment}, driving_moment: {equilibrium_terms.driving_moment}, resisting_force: {equilibrium_terms.resisting_force}, driving_force: {equilibrium_terms.driving_force}')

print("-" * 30)

