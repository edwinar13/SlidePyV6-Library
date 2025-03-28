from slidepyv6 import SlideProject

# Create a new project
project = SlideProject("example_project.slim")


# Cargas del proyecto
loads  = project.loads
linear_loads = loads.linear
distributed_loads= loads.distributed
print("-" * 30)
print(f'{"→ Cargas lineales"}')
for l_load in loads.linear:
    
    id = l_load.id
    x = l_load.load.point.x
    y  = l_load.load.point.y    
    magnitude = l_load.load.magnitude
    angle = l_load.angle
    type_load = l_load.type_load
    print(f'id: {id}, point1: ({x}, {y}), angle: {angle}, type_load: {type_load}, magnitude: {magnitude}')
print("-" * 30)
print(f'{"→ Cargas distribuidas"}')
for d_load in loads.distributed:
    
    id = d_load.id

    x1 = d_load.load.point.x
    y1 = d_load.load.point.y
    magnitude1 = d_load.load.magnitude

    x2 = d_load.load2.point.x
    y2 = d_load.load2.point.y
    magnitude2 = d_load.load2.magnitude

    angle = d_load.angle
    type_load = d_load.type_load
    print(f'id: {id}, point1: ({x1}, {y1}), point2: ({x2}, {y2}), angle: {angle}, type_load: {type_load}, magnitude1: {magnitude1}, magnitude2: {magnitude2}')
print("-" * 30)


