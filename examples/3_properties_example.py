from slidepyv6 import SlideProject, MohrCoulombParams, EndAnchoredParams

# Create a new project
project = SlideProject("example_project.slim")


# propiedades de los materiales del proyecto
materials = project.properties.materials

for material in materials:
    id = material.id
    name = material.name
    colorRGB = material.color.red, material.color.green, material.color.blue
    hatch = material.hatch
    unit_weight = material.unit_weight
    satured_unit_weight = material.satured_unit_weight
    material_params = material.material_params
    is_mohr_coulomb = isinstance(material_params, MohrCoulombParams)
    print(f'id: {id}, name: {name}, colorRGB: {colorRGB}, hatch: {hatch}, unit_weight: {unit_weight}, satured_unit_weight: {satured_unit_weight}, material_params: {material_params}, is_mohr_coulomb: {is_mohr_coulomb}')



# propiedades de los anclajes del proyecto
support = project.properties.supports

for support in support:
    id = support.id
    name = support.name
    colorRGB = support.color.red, support.color.green, support.color.blue
    support_params = support.support_params
    is_end_anchored = isinstance(support_params, EndAnchoredParams)
    print(f'id: {id}, name: {name}, colorRGB: {colorRGB}, support_params: {support_params}, is_end_anchored: {is_end_anchored}')



