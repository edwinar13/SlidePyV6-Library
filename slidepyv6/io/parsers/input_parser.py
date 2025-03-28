from ...models.metadata import ProjectMetadata
from ...models.geometries import ProjectGeometry
from ...models.properties import ProjectProperties, PropertyMaterial, PropertySupport
from ...models.loads import ProjectLoads
from ...models.properties import MohrCoulombParams, UndrainedParams, NoStrengthParams, InfiniteStrengthParams, HoekBrownParams, GeneralHoekBrownParams
from ...models.properties import EndAnchoredParams, GeoTextileParams, GroutedTiebackParams, GroutedTiebackFrictionParams, MicroPileParams, SoilNailParams
from ...models.geometries import Vertex, Cell, Point, Support
from ...models.loads import LinearLoad, DistributedLoad, Load
from ...models.properties import Color

import re
from typing import Tuple


class InputParser:
    @staticmethod
    def parse(content: str) -> Tuple[ProjectMetadata, ProjectProperties, ProjectGeometry, ProjectLoads]:
        """
        Parsea el contenido del archivo de entrada
        
        Args:
            content: Contenido del archivo como string
        """
        # Asegurarnos que content sea string
        #------------------------------------------------
        if isinstance(content, bytes):
            content = content.decode('utf-8', errors='ignore')
        
        # Separar el contenido en secciones
        #------------------------------------------------
        sections = [
            "model description",
            "material types",
            "anchor types",
            "vertices",
            "cells",
            "anchors",
            "water table",
            "slope",
            "exterior",
            "forces",
            "slope limits",
            "material properties"
        ]

        extracted_data = {}        
        for section in sections:
            pattern = rf"^{section}\b:(.*?)(?=\n\w|\Z)"
            match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
            if match:
                extracted_data[section] = match.group(1).strip()
 
        # Parsear cada sección
        #------------------------------------------------
        project_metadata = InputParser._parse_project_metadata(
            content=extracted_data['model description'])
        
        project_properties = InputParser._parse_project_properties(
            material_styles=extracted_data['material properties'],
            material_properties=extracted_data['material types'],
            anchor_properties=extracted_data['anchor types']
            )
         
        project_geometry, project_loads = InputParser._parse_project_geometry(
                vertices=extracted_data['vertices'],
                cells=extracted_data['cells'],
                anchors=extracted_data['anchors'],
                water_table=extracted_data['water table'],
                slope=extracted_data['slope'],
                exterior=extracted_data['exterior'],
                forces=extracted_data['forces'],
                slope_limits=extracted_data['slope limits']                
            )     
        
        return (project_metadata,project_properties, project_geometry, project_loads)  

    def _parse_project_metadata(content: str) -> ProjectMetadata:
        lines = content.splitlines()
        data = {}
        for i, line in enumerate(lines):
            key, value = line.split(':',1)
            data[key.strip()] = value.strip()

        return ProjectMetadata(
            version=data['version'],
            title=data['title'],
            analysis=data['str_analysis'],
            author=data['str_author'],
            date=data['str_date_created'],
            company=data['str_company'],
            comments=[data['str_comments1'],data['str_comments2'], data['str_comments3'], data['str_comments4'], data['str_comments5']],
            units=data['units'],
            time_units=data['time_units'],
            permeability_units_imperial=data['permeability_units_imperial'],
            permeability_units_metric=data['permeability_units_metric'],
            direction=data['direction'],
            nummaterials=int(data['nummaterials']),
            numanchors=int(data['numanchors']),

            seismic=float(data['seismic']),
            seismicv=float(data['seismicv'])
            
        )

    def _parse_project_properties(
            material_styles: str,
            material_properties: str,
            anchor_properties: str
            ) -> ProjectProperties:

        # convertir material_styles a diccionario
        #------------------------------------------------
        lines = material_styles.splitlines()
        regular_expression = r'^(.*?)\s+red:\s*(\d+)\s+green:\s*(\d+)\s+blue:\s*(\d+)(?:\s+hatch:\s*(\d+))?'
        material_styles_dict = {}
        n= 1
        m= 1
        for i, line in enumerate(lines):
            match = re.match(regular_expression, line)
            if match:
                material_name = match.group(1).strip()
                red = int(match.group(2))
                green = int(match.group(3))
                blue = int(match.group(4))
                hatch = match.group(5) if match.group(5) else None
                if hatch is not None:
                    index = f'soil{n}'
                    material_styles_dict[index] = {'name':material_name,'red': red, 'green': green, 'blue': blue, 'hatch': hatch}
                    n += 1
                else:
                    index = f'anchor{m}'
                    material_styles_dict[index] = {'name':material_name,'red': red, 'green': green, 'blue': blue}
                    m += 1


        #------------------------------------------------
        # material properties 
        #------------------------------------------------
        lines = material_properties.splitlines()
        materials = []
        for i, line in enumerate(lines):      

            #data_material  → dict
            data_material  = line.strip().split(' ') [2:]     
            data_material_dict = {data_material[i].rstrip(':'): data_material[i+1] for i in range(0, len(data_material), 2)} 
            if 'uwbwt' not in data_material_dict:
                data_material_dict['uwbwt'] = 'None'


            id_material = line.strip().split(' ')[0]
            type_material = data_material_dict['type'] 
            unit_weight = data_material_dict['uw']
            satured_unit_weight = data_material_dict['uwbwt']

            
            name = material_styles_dict[id_material]['name']
            color = Color(
                red= material_styles_dict[id_material]['red'],
                green= material_styles_dict[id_material]['green'],
                blue= material_styles_dict[id_material]['blue']
            )
            hatch = material_styles_dict[id_material]['hatch']
                         

            if type_material == '0': # Mohr Coulomb               
                cohesion = data_material_dict['c']
                friction_angle = data_material_dict['phi']  
                model = MohrCoulombParams(
                                cohesion= float(cohesion),
                                friction_angle= float(friction_angle),                                
                            )               

            elif type_material == '1': # Undrained   
                cohesion = data_material_dict['c']
                c_type = data_material_dict['ctype']
                model =  UndrainedParams(
                                cohesion= float(cohesion),
                                c_type= int(c_type)
                            )                    

            elif type_material == '2': # No Strength
                model = NoStrengthParams()

            elif type_material == '3': # Infinite Strength
                model = InfiniteStrengthParams()

            elif type_material == '7': # Hoek Brown

                sigc = data_material_dict['sigc']
                mb = data_material_dict['mb']
                s = data_material_dict['s']
                model = HoekBrownParams(                               
                                sigc= float(sigc),
                                mb= float(mb),
                                s= float(s)
                            )

            elif type_material == '8': # General Hoek Brown
                sigc = data_material_dict['sigc']
                mb = data_material_dict['mb']
                s = data_material_dict['s']
                a = data_material_dict['a']
                model = GeneralHoekBrownParams(                                
                                sigc= float(sigc),
                                mb= float(mb),
                                s= float(s),
                                a= float(a)
                            )            
      
            materials.append(PropertyMaterial(
                        id= id_material,
                        name= name,
                        color= color,
                        hatch= hatch,
                        unit_weight= float(unit_weight),
                        satured_unit_weight= float(satured_unit_weight) if satured_unit_weight != 'None' else None,
                        material_params= model 
            ))                    

       
        #------------------------------------------------
        # material properties 
        #------------------------------------------------

        lines = anchor_properties.splitlines()
        supports = []
        for i, line in enumerate(lines):

            #data_anchor  → dict
            data_anchor  = line.strip().split(' ') [2:]
            data_anchor_dict = {data_anchor[i].rstrip(':'): data_anchor[i+1] for i in range(0, len(data_anchor), 2)}
            
            id_anchor = line.strip().split(' ')[0]
            type_anchor = data_anchor_dict['type']
            name = material_styles_dict[id_anchor]['name']
            color = Color(
                red= material_styles_dict[id_anchor]['red'],
                green= material_styles_dict[id_anchor]['green'],
                blue= material_styles_dict[id_anchor]['blue']
            )
            # print(data_anchor_dict)
            if type_anchor == '1': # End Anchored
                fa = data_anchor_dict['fa']
                sp = data_anchor_dict['sp']
                cap = data_anchor_dict['cap']
                model = EndAnchoredParams(
                                fa= int(fa),
                                sp= float(sp),
                                cap= float(cap)
                            )            
            elif type_anchor == '4': # Geo-Textile
                fa = data_anchor_dict['fa']
                ts = data_anchor_dict['ts']
                po_adh = data_anchor_dict['po_adh']
                po_fric = data_anchor_dict['po_fric']
                model = GeoTextileParams(
                                fa= int(fa),
                                ts= float(ts),
                                po_adh= float(po_adh),
                                po_fric= float(po_fric)
                            )            
            elif type_anchor == '2': # Grouted Tieback
                fa = data_anchor_dict['fa']
                sp = data_anchor_dict['sp']
                cap = data_anchor_dict['cap']
                pc = data_anchor_dict['pc']
                bs = data_anchor_dict['bs']
                bt = data_anchor_dict['bt']
                bl = data_anchor_dict['bl']
                model = GroutedTiebackParams(
                                fa= int(fa),
                                sp= float(sp),
                                cap= float(cap),
                                pc= float(pc),
                                bs= float(bs),
                                bt= int(bt),
                                bl= float(bl)
                            )
            elif type_anchor == '5': # Grouted Tieback Friction
                fa = data_anchor_dict['fa']
                sp = data_anchor_dict['sp']
                cap = data_anchor_dict['cap']
                pc = data_anchor_dict['pc']
                bt = data_anchor_dict['bt']
                bl = data_anchor_dict['bl']
                po_adh = data_anchor_dict['po_adh']
                po_fric = data_anchor_dict['po_fric']
                model = GroutedTiebackFrictionParams(
                                fa= int(fa),
                                sp= float(sp),
                                cap= float(cap),
                                pc= float(pc),
                                bt= int(bt),
                                bl= float(bl),
                                po_adh= float(po_adh),
                                po_fric= float(po_fric)
                            )
            elif type_anchor == '6': # Micro Pile
                fa = data_anchor_dict['fa']
                sp = data_anchor_dict['sp']
                mpss = data_anchor_dict['mpss']
                mpforcedirection = data_anchor_dict['mpforcedirection']
                model = MicroPileParams(
                                fa= int(fa),
                                sp= float(sp),
                                mpss= float(mpss),
                                mpforcedirection= int(mpforcedirection)
                            )
            elif type_anchor == '3': # Soil Nail
                fa = data_anchor_dict['fa']
                sp = data_anchor_dict['sp']
                cap = data_anchor_dict['cap']
                pc = data_anchor_dict['pc']
                bs = data_anchor_dict['bs']
                model = SoilNailParams(
                                fa= int(fa),
                                sp= float(sp),
                                cap= float(cap),
                                pc= float(pc),
                                bs= float(bs)
                            )      

            # ------------------------------------------------
            supports.append(PropertySupport(
                                id= id_anchor,
                                name= name,
                                color= color,
                                support_params= model
                            ))
                


        return ProjectProperties(materials=materials, supports=supports)

    def _parse_project_geometry(
                vertices: str,
                cells: str,
                anchors: str,
                water_table: str,
                slope: str,
                exterior: str,
                forces: str,
                slope_limits: str ) -> tuple [ProjectGeometry, ProjectLoads]:
        
        #------------------------------------------------
        # vertices
        # ------------------------------------------------
        lines = vertices.splitlines()
        list_vertices = []
        for i, line in enumerate(lines):
            data_vertex  = line.strip().split(' ')
            num = data_vertex[0]
            x = data_vertex[2]
            y = data_vertex[5]
            point = Point(x=float(x), y=float(y))
            list_vertices.append(Vertex(
                id= int(num),
                point= point
            ))
        
        #------------------------------------------------
        # cells
        # ------------------------------------------------
        lines = cells.splitlines()
        list_cells = []
        for i, line in enumerate(lines):
            data_cell  = line.strip().split(' ')
            num = data_cell[0]
            vertices_id = data_cell[3].strip('[]').split(',')

            cell_list_vertices = []
            for i in range(len(vertices_id)):
                vertices_id[i] = int(vertices_id[i])
                cell_list_vertices.append(list_vertices[vertices_id[i]-1])           

            material = data_cell[-1]
            list_cells.append(Cell(
                id= int(num),
                vertices= cell_list_vertices,
                property_id= material
            ))
        
        #------------------------------------------------
        # supports
        # ------------------------------------------------
        lines = anchors.splitlines()
        list_anchors = []
        for i, line in enumerate(lines):
            data_anchor  = line.strip().split(' ')            
            num = data_anchor[0]
            x1 = data_anchor[2]
            y1 = data_anchor[4]
            x2 = data_anchor[6]
            y2 = data_anchor[8]
            list_anchors.append(Support(
                id= int(num),
                point1= Point(x=float(x1), y=float(y1)),
                point2= Point(x=float(x2), y=float(y2)),
                property_id= data_anchor[-5],
            ))  
        
        #------------------------------------------------
        # water table
        # ------------------------------------------------
        if water_table.strip():           
            list_water_table_vertices = []
            data_water_table  = water_table.split(':', 1)[1].strip().strip('[]').split(',')
            for i in range(len(data_water_table)):
                data_water_table_id = int(data_water_table[i])
                list_water_table_vertices.append(
                    list_vertices[data_water_table_id-1]
                )
        else:
            list_water_table_vertices = []
        
        #------------------------------------------------
        # slope limits
        # ------------------------------------------------
        if slope_limits != '':
            data_slope_limits  = slope_limits.strip().split(' ')
            x1 = data_slope_limits[1]
            y1 = data_slope_limits[3]
            x2 = data_slope_limits[5]
            y2 = data_slope_limits[7]
            tuple_points = (Point(x=float(x1), y=float(y1)), Point(x=float(x2), y=float(y2)))
            slope_limits = tuple_points
            
        else:
            slope_limits = None

        #------------------------------------------------
        # slope
        # ------------------------------------------------
        if slope.strip():            
            list_slope_vertices = []
            data_slope  = slope.split(':', 1)[1].strip().strip('[]').split(',')
            for i in range(len(data_slope)):
                data_slope_id = int(data_slope[i])
                list_slope_vertices.append(
                    list_vertices[data_slope_id-1]
                )                
        else:
            list_slope_vertices = []
        
        #------------------------------------------------
        # exterior
        # ------------------------------------------------   
        if exterior.strip():            
            list_exterior_vertices = []
            data_exterior  = exterior.split(':', 1)[1].strip().strip('[]').split(',')
            for i in range(len(data_exterior)):
                data_exterior_id = int(data_exterior[i])
                list_exterior_vertices.append(
                    list_vertices[data_exterior_id-1]
                )
        else:
            list_exterior_vertices = []

        #------------------------------------------------
        # forces
        # ------------------------------------------------
        lines = forces.splitlines()
        list_linear_loads = []
        list_distributed_loads = []
        for i, line in enumerate(lines):
            data_force  = line.strip().split(' ')
            num = data_force[0]
            type_load = data_force[2]
            if type_load == '1': # Linear Load
                x1 = data_force[4]
                y1 = data_force[6]
                angle = data_force[8]
                load = data_force[10]
                list_linear_loads.append(LinearLoad(
                    id= int(num),
                    type_load= int(type_load),
                    angle= float(angle),
                    load= Load(
                        point= Point(x=float(x1), y=float(y1)),
                        magnitude = float(load)
                    )
                ))

            elif type_load == '0': # Distributed Load
                x1 = data_force[4]
                y1 = data_force[6]
                x2 = data_force[8]
                y2 = data_force[10]
                angle = data_force[12]
                load = data_force[14]
                load2 = data_force[16]
                list_distributed_loads.append(DistributedLoad(
                    id= int(num),
                    type_load= int(type_load),
                    angle= float(angle),
                    load= Load(
                        point= Point(x=float(x1), y=float(y1)),
                        magnitude= float(load)
                    ),
                    load2= Load(
                        point= Point(x=float(x2), y=float(y2)),
                        magnitude= float(load2)
                    )
                ))

        #------------------------------------------------
        
        project_loads = ProjectLoads(
                linear = list_linear_loads, 
                distributed = list_distributed_loads
            )
              
        project_geometry =ProjectGeometry(
            vertex= list_vertices,
            cells= list_cells,
            supports= list_anchors,
            water_table_vertex= list_water_table_vertices,
            limits= slope_limits,
            slope= list_slope_vertices,
            exterior= list_exterior_vertices
        )

        return project_geometry, project_loads
