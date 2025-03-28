from slidepyv6 import SlideProject, MohrCoulombParams, EndAnchoredParams

# Create a new project
project = SlideProject("example_project.slim")


# Geometria del proyecto
geometry  = project.geometry

# Vértices
vertex  = geometry.vertex
length = len(vertex)
print("-" * 30)
print(f'Número de vértices: {length}')
print(f'{"Vértices"}')
for vertex in vertex:
    id = vertex.id
    point = vertex.point
    x = point.x
    y = point.y
    print(f'id: {id}, x: {x}, y: {y}')
    
# Celdas
cells = geometry.cells
length = len(cells)
print("-" * 30)
print(f'Número de celdas: {length}')
print(f'{"→ Celdas"}')
for cell in cells:
    id = cell.id
    vertices = cell.vertices
    print(f'celda id: {id}      <<< vertices id: [{vertices[0].id}, {vertices[1].id}, {vertices[2].id}] >>>')


# Exterior
exterior = geometry.exterior
print("-" * 30)
print(f'{"→ Exterior"}')
for exterior in exterior:
    print(f'vertice id: {exterior.id}')

# Pendiente
slope = geometry.slope
print("-" * 30)
print(f'{"→ Pendiente"}')
for slope in slope:
    print(f'vertice id: {slope.id}')


# Límites
limits = geometry.limits
p1 = limits[0]
p2 = limits[1]
print("-" * 30)
print(f'{"→ Límites"}')
print(f'p1: [{p1.x}, {p1.y}]')
print(f'p2: [{p2.x}, {p2.y}]')


# Nivel freático
water_table_vertex = geometry.water_table_vertex
print("-" * 30)
print(f'{"→ Nivel freático"}')
for water_table_vertex in water_table_vertex:
    print(f'vertice id: {water_table_vertex.id}')


# Soportes
supports = geometry.supports
length = len(supports)
print("-" * 30)
print(f'Número de soportes: {length}')
print(supports)
for support in supports:
    id = support.id
    point1 = support.point1
    x1 = point1.x
    y1 = point1.y
    point2 = support.point2
    x2 = point2.x
    y2 = point2.y
    property_id = support.property_id
    print(f'id: {id}, point1: ({x1}, {y1}), point2: ({x2}, {y2}), property_id: {property_id}')



