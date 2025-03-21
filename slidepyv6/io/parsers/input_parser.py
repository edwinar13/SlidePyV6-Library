from ...models.metadata import ProjectMetadata
from ...models.geometries import ProjectGeometry
from ...models.properties import ProjectProperties, PropertyMaterial, PropertySupport
from ...models.loads import ProjectLoads
from ...models.properties import MohrCoulombParams, UndrainedParams, NoStrengthParams, InfiniteStrengthParams, HoekBrownParams, GeneralHoekBrownParams
from ...models.properties import EndAnchoredParams, GeoTextileParams, GroutedTiebackParams, GroutedTiebackFrictionParams, MicroPileParams, SoilNailParams
from ...models.geometries import Vertex, Cell, Point, Support
from ...models.loads import Force
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
            key, value = line.split(':')
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
                '''
                {'type': '1', 'fa': '0', 'sp': '1', 'cap': '100'}
                {'type': '1', 'fa': '1', 'sp': '1', 'cap': '100'}
                '''
                fa = data_anchor_dict['fa']
                sp = data_anchor_dict['sp']
                cap = data_anchor_dict['cap']
                model = EndAnchoredParams(
                                fa= int(fa),
                                sp= float(sp),
                                cap= float(cap)
                            )            
            elif type_anchor == '4': # Geo-Textile
                '''
                {'type': '4', 'fa': '1', 'ts': '40', 'fo_flag': '3', 'fo_ang': '30', 'anch': '2', 'po_type': '0', 'po_adh': '5', 'po_fric': '40', 'cov_perc': '100', 'ss_mod': '1'}
                {'type': '4', 'fa': '0', 'ts': '40', 'fo_flag': '3', 'fo_ang': '30', 'anch': '2', 'po_type': '0', 'po_adh': '5', 'po_fric': '40', 'cov_perc': '100', 'ss_mod': '1'}
                '''
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
                '''
                {'type': '2', 'fa': '1', 'sp': '1', 'cap': '100', 'pc': '100', 'bst': '0', 'bs': '50', 'bt': '0', 'bl': '2', 'shear_cap_flag': '0', 'shear_cap': '0', 'comp_cap_flag': '0', 'comp_cap': '0'}
                {'type': '2', 'fa': '0', 'sp': '1', 'cap': '100', 'pc': '100', 'bst': '0', 'bs': '50', 'bt': '1', 'bl': '10', 'shear_cap_flag': '0', 'shear_cap': '0', 'comp_cap_flag': '0', 'comp_cap': '0'}
                '''
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
                '''
                {'type': '5', 'fa': '1', 'sp': '1', 'cap': '100', 'pc': '100', 'bt': '0', 'bl': '2', 'po_type': '0', 'po_adh': '5', 'po_fric': '40', 'g_diam': '0.1', 'ss_mod': '1', 'shear_cap_flag': '0', 'shear_cap': '0', 'comp_cap_flag': '0', 'comp_cap': '0'}
                {'type': '5', 'fa': '0', 'sp': '1', 'cap': '100', 'pc': '100', 'bt': '0', 'bl': '0.1', 'po_type': '0', 'po_adh': '5', 'po_fric': '40', 'g_diam': '0.1', 'ss_mod': '1', 'shear_cap_flag': '0', 'shear_cap': '0', 'comp_cap_flag': '0', 'comp_cap': '0'}
                ''' 
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
                '''
                {'type': '6', 'fa': '1', 'sp': '1', 'mpss': '20', 'mpforcedirection': '1'}
                {'type': '6', 'fa': '0', 'sp': '1', 'mpss': '20', 'mpforcedirection': '0'}
                '''
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
                '''
                {'type': '3', 'fa': '0', 'sp': '1', 'cap': '100', 'pc': '100', 'bst': '0', 'bs': '50', 'shear_cap_flag': '0', 'shear_cap': '0', 'comp_cap_flag': '0', 'comp_cap': '0'}
                {'type': '3', 'fa': '1', 'sp': '1', 'cap': '100', 'pc': '100', 'bst': '0', 'bs': '50', 'shear_cap_flag': '0', 'shear_cap': '0', 'comp_cap_flag': '0', 'comp_cap': '0'}
                '''
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
        '''
        1 x1: 28.3042715040913 y1: 10.0968796746731 x2: 23.3042715040913 y2: 10.0968796746731  material: anchor8 group_id: -1 index_in_group: -1
        2 x1: 28.3042715040913 y1: 10.0968796746731 x2: 23.3042715040913 y2: 10.0968796746731  material: anchor8 group_id: -1 index_in_group: -1
        3 x1: 28.2623346286052 y1: 10.5162484295336 x2: 23.2623346286052 y2: 10.5162484295336  material: anchor8 group_id: -1 index_in_group: -1
        '''
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
        # vertices: [39,40,41,42,43,11,10,44,28,45,46,47]
 
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
        #print(slope_limits)
        #x1: 0 y1: 23.3275292619621 x2: 39.4244071217067 y2: 7.30382375586473
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
        # 1  vertices: [17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,25,24,23,22]

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
        # #1  vertices: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]         

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
        '''
        1 type: 0 x1: 20.8462083795773 y1: 14.8442 x2: 20.7642411664626 y2: 14.8414 angle: 271.956463062261 load: 15 load2: 15 stage2: 0 design_standard_option: 0
        2 type: 0 x1: 20.7642411664626 y1: 14.8414 x2: 19.0882889309567 y2: 14.7856 angle: 271.906930196748 load: 15 load2: 15 stage2: 0 design_standard_option: 0
        3 type: 0 x1: 19.0882889309567 y1: 14.7856 x2: 16.8462083795773 y2: 14.710844253146 angle: 271.909656029285 load: 15 load2: 15 stage2: 0 design_standard_option: 0
        4 type: 0 x1: 26.8462083795773 y1: 14.7108 x2: 22.8462083795773 y2: 14.8441775864794 angle: 268.090214391141 load: 15 load2: 15 stage2: 0 design_standard_option: 0
        '''
        lines = forces.splitlines()
        list_forces = []
        for i, line in enumerate(lines):
            data_force  = line.strip().split(' ')
            #print(data_force)
            #['1', 'type:', '0', 'x1:', '20.8462083795773', 'y1:', '14.8442', 'x2:', '20.7642411664626', 'y2:', '14.8414', 'angle:', '271.956463062261', 'load:', '15', 'load2:', '15', 'stage2:', '0', 'design_standard_option:', '0']
            num = data_force[0]
            type_load = data_force[2]
            x1 = data_force[4]
            y1 = data_force[    6]
            x2 = data_force[8]
            y2 = data_force[10]
            angle = data_force[12]
            load = data_force[14]
            load2 = data_force[16]
            list_forces.append(Force(
                id= int(num),
                point1= Point(x=float(x1), y=float(y1)),
                point2= Point(x=float(x2), y=float(y2)),
                angle= float(angle),
                type_load= int(type_load),
                load= float(load),
                load2= float(load2)
            ))       
        
        #------------------------------------------------
        #------------------------------------------------
        
        project_loads = ProjectLoads(forces= list_forces)
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




    

'''



    @staticmethod
    def _parse_project_settings(lines: list) -> ProjectSettings:
        # Lógica específica para settings
        return ProjectSettings(...)

    @staticmethod
    def _parse_vertices(lines: list) -> list[Vertice]:
        # Lógica para vértices
        return [Vertice(...), ...]
       

    def _parse_input_file(self) -> None:
        """Parsea el archivo principal de configuración (input)"""
        input_content = self._io.read_project_file('input')
        
        # Si input_content es bytes, decodificarlo
        if isinstance(input_content, bytes):
            input_content = input_content.decode('utf-8', errors='ignore')
        # Si ya es str, usarlo directamente
        
        lines = input_content.splitlines()

        input_data = SlideInputData(
            version="",
            project_settings=None,
            soil_parameters=[],
            anchor_parameters=[],
            geometry=None
        )
        vertices = []
        cells = []
        anchors = []
        water_table = []
        slope = []
        exterior = []
        forces = []
        slope_limits = None

        # parsear los parametros de suelo
        soil_parameters = []
        anchor_parameters = []
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            #print(f"linea {i}: {line}")

            if line.startswith('model description:'):

                # version
                input_data.version = lines[i+1].strip()

                # general settings
                units = lines[i+4].split(':')[1].strip()
                time_units = lines[i+52].split(':')[1].strip()
                permeability_units_imperial = lines[i+53].split(':')[1].strip()
                permeability_units_metric = lines[i+54].split(':')[1].strip()
                direction = lines[i+8].split(':')[1].strip()
                nummaterials = lines[i+37].split(':')[1].strip()
                numanchors = lines[i+38].split(':')[1].strip()
                general_settings = GeneralSettings(
                    units=units,
                    time_units=time_units,
                    permeability_units_imperial=permeability_units_imperial,
                    permeability_units_metric=permeability_units_metric,
                    direction=direction,
                    nummaterials=nummaterials,
                    numanchors=numanchors
                )
                # summary settings
                title = lines[i+2].split(':')[1].strip()[1:-1]
                analysis = lines[i+55].split(':')[1].strip()
                author = lines[i+56].split(':')[1].strip()
                date = lines[i+57].split(',')[0].strip().split(':')[1].strip()
                company = lines[i+58].split(':')[1].strip()
                comments1 = lines[i+59].split(':')[1].strip()
                comments2 = lines[i+60].split(':')[1].strip()
                comments3 = lines[i+61].split(':')[1].strip()
                comments4 = lines[i+62].split(':')[1].strip()
                comments5 = lines[i+63].split(':')[1].strip()
                summary_settings = SummarySettings(
                    title=title,
                    analysis=analysis,
                    author=author,
                    date=date,
                    company=company,
                    comments1=comments1,
                    comments2=comments2,
                    comments3=comments3,
                    comments4=comments4,
                    comments5=comments5
                )

                # seismic settings
                seismic = lines[i+5].split(':')[1].strip()
                seismicv = lines[i+6].split(':')[1].strip()
                seismic_settings = SeismicSettings(
                    seismic=seismic,
                    seismicv=seismicv
                )

                input_data.project_settings = ProjectSettings(
                    general_settings=general_settings,
                    summary_settings=summary_settings,
                    seismic_settings=seismic_settings
                )

            elif line.startswith('vertices:'):
                j = i+1
                line = lines[j].strip()
                while line != '':

                    num = line.split(' ')[0]
                    x = line.split(' ')[2]
                    y = line.split(' ')[-1]
                    vertices.append(Vertice(
                        num_vertice=int(num),
                        x=float(x),
                        y=float(y)
                    ))

                    j += 1
                    line = lines[j].strip()
     

            elif line.startswith('cells:'):
                j = i+1
                line = lines[j].strip()
                while line != '':
                    num = line.split(' ')[0]
                    cell_vertices = line.split(' ')[-3].strip('[]').split(',')
                    cell_material = line.split(' ')[-1]
                    cells.append(Cell(
                        num_cell=num,
                        vertices=cell_vertices,
                        material=cell_material
                    ))
                    j += 1
                    line = lines[j].strip()     
                    
            elif line.startswith('anchors:'):
                j = i+1
                line = lines[j].strip()
                while line != '':
                    anchor_material = line.split('  ')[1].split(' ')[1]
                    data = line.split('  ')[0].split(' ')
                    num = data[0]
                    x1 = data[2]
                    y1 = data[4]
                    x2 = data[6]
                    y2 = data[8]

                    anchors.append(Anchor(
                        num_anchor_=num,
                        x1=float(x1),
                        y1=float(y1),
                        x2=float(x2),
                        y2=float(y2),
                        material=anchor_material
                    ))
                    j += 1
                    line = lines[j].strip()

            elif line.startswith('water table:'):
                j = i+1
                line = lines[j].strip()
                water_table = line.split(' ')[-1].strip('[]').split(',')

            elif line.startswith('slope:'):
                j = i+1
                line = lines[j].strip()
                slope = line.split(' ')[-1].strip('[]').split(',')

            elif line.startswith('exterior:'):
                j = i+1
                line = lines[j].strip()
                exterior = line.split(' ')[-1].strip('[]').split(',')

            elif line.startswith('forces:'):
                j = i+1
                line = lines[j].strip()
                while line != '':
                    data = line.split('stage')[0].strip().split(' ')
                    
                    num = data[0]
                    force_type = data[2]
                    x1 = data[4]
                    y1 = data[6]

                    if force_type == '0':
                        x2 = data[8]
                        y2 = data[10]
                        angle = data[12]
                        load = data[14]
                        load2 = data[16]
                    elif force_type == '1':
                        x2 = 0
                        y2 = 0
                        angle = data[8]
                        load = data[10]
                        load2 = 0
                    
                    forces.append(Force(
                        num_force=num,
                        force_type=force_type,
                        x1=float(x1),
                        y1=float(y1),
                        x2=float(x2),
                        y2=float(y2),
                        angle=float(angle),
                        load=float(load),
                        load2=float(load2)
                    ))

                    j += 1
                    line = lines[j].strip()

            elif line.startswith('slope limits:'):
                j = i+1
                line = lines[j].strip()
                slope_limits = line.split(' ')
                slope_limits = (
                    GeometryPoint(x=float(slope_limits[1]), y=float(slope_limits[3])),
                    GeometryPoint(x=float(slope_limits[5]), y=float(slope_limits[7]))
                )

            elif line.startswith('material types:'):
                j = i+1
                line = lines[j].strip()
                while line != '':
                    data_soil = line.split(' ')                  
                    soil_number = data_soil[0]
                    soil_type_number = data_soil[3]

                    if soil_type_number == '0': # Mohr Coulomb
                        # ['soil1', '=', 'type:', '0', 'water:', '0.5', 'wtable:', '1', 'c:', '1', 'phi:', '35', 'uw:', '20', 'uwbwt:', '21', 'hutype:', '0', 'withru:', '0.5']
                        unit_weight = data_soil[13]
                        satured_unit_weight = data_soil[15]
                        cohesion = data_soil[9]
                        friction_angle = data_soil[11]
                        soil_parameters.append(SoilParameterMohrCoulomb(
                            soil_name=soil_number,
                            soil_style=None,
                            soil_number=soil_number,
                            soil_type_number=soil_type_number,
                            unit_weight=float(unit_weight),
                            satured_unit_weight=float(satured_unit_weight),
                            cohesion=float(cohesion),
                            friction_angle=float(friction_angle)
                        ))
                    
                    elif soil_type_number == '1': # Undrained
                        # ['soil2', '=', 'type:', '1', 'ctype:', '0', 'c:', '11', 'uw:', '20', 'uwbwt:', '22', 'withru:', '0']
                        unit_weight = data_soil[9]
                        satured_unit_weight = data_soil[11]
                        cohesion = data_soil[7]
                        soil_parameters.append(SoilParameterUndrained(
                            soil_name=soil_number,
                            soil_style=None,
                            soil_number=soil_number,
                            soil_type_number=soil_type_number,
                            unit_weight=float(unit_weight),
                            satured_unit_weight=float(satured_unit_weight),
                            cohesion=float(cohesion)
                        ))

                    elif soil_type_number == '2': # No Strength
                        # data_soil: ['soil3', '=', 'type:', '2', 'uw:', '20', 'uwbwt:', '22', 'withru:', '0']
                        unit_weight = data_soil[7]
                        satured_unit_weight = data_soil[9]
                        soil_parameters.append(SoilParameterNoStrength(
                            soil_name=soil_number,
                            soil_style=None,
                            soil_number=soil_number,
                            soil_type_number=soil_type_number,
                            unit_weight=float(unit_weight),
                            satured_unit_weight=float(satured_unit_weight)
                        ))

                    elif soil_type_number == '3': # Infinite Strength
                        # data_soil: ['soil4', '=', 'type:', '3', 'uw:', '20', 'uwbwt:', '22', 'withru:', '0']
                        #           ['soil19', '=', 'type:', '3', 'uw:', '24', 'withru:', '0']
                        unit_weight = data_soil[7]
                        satured_unit_weight = data_soil[9]
                        soil_parameters.append(SoilParameterInfiniteStrength(
                            soil_name=soil_number,
                            soil_style=None,
                            soil_number=soil_number,
                            soil_type_number=soil_type_number,
                            unit_weight=float(unit_weight),
                            satured_unit_weight=float(satured_unit_weight)
                        ))
                    
                    elif soil_type_number == '7': # Hoek Brown
                        # data_soil: ['soil5', '=', 'type:', '7', 'water:', '1', 'wtable:', '1', 'mb:', '2', 's:', '0.01', 'a:', '0.5', 'sigc:', '90', 'uw:', '20', 'uwbwt:', '20', 'hutype:', '0', 'withru:', '0']
                        unit_weight = data_soil[17]
                        satured_unit_weight = data_soil[19]
                        sigc = data_soil[15]
                        mb = data_soil[9]
                        s = data_soil[11]
                        soil_parameters.append(SoilParameterHoekBrown(
                            soil_name=soil_number,
                            soil_style=None,
                            soil_number=soil_number,
                            soil_type_number=soil_type_number,
                            unit_weight=float(unit_weight),
                            satured_unit_weight=float(satured_unit_weight),
                            sigc=float(sigc),
                            mb=float(mb),
                            s=float(s)
                        ))
                    
                    elif soil_type_number == '8': # General Hoek Brown
                        # data_soil: ['soil6', '=', 'type:', '8', 'water:', '1', 'wtable:', '1', 'mb:', '2', 's:', '0.01', 'a:', '0.5', 'sigc:', '90', 'uw:', '20', 'uwbwt:', '20', 'hutype:', '0', 'withru:', '0']
                        
                        unit_weight = data_soil[17 ]
                        satured_unit_weight = data_soil[19]
                        sigc = data_soil[15]
                        mb = data_soil[9]
                        s = data_soil[11]
                        a = data_soil[13]
                        soil_parameters.append(SoilParameterGenHoekBrown(
                            soil_name=soil_number,
                            soil_style=None,
                            soil_number=soil_number,
                            soil_type_number=soil_type_number,
                            unit_weight=float(unit_weight),
                            satured_unit_weight=float(satured_unit_weight),
                            sigc=float(sigc),
                            mb=float(mb),
                            s=float(s),
                            a=float(a)
                        ))

                    j += 1
                    line = lines[j].strip()
                
                input_data.soil_parameters = soil_parameters

            elif line.startswith('anchor types:'):
                j = i+1
                line = lines[j].strip()
                
                while line != '':
                    data = line.split(' ')  
                    # ['anchor20', '=', 'type:', '1', 'fa:', '0', 'sp:', '1', 'cap:', '100']
                    anchor_number = data[0]
                    anchor_type_number = data[3]          
                    
                    if anchor_type_number == '1': # end anchored
                        anchor_parameters.append(AnchorParameterEndAnchored(
                            anchor_name=anchor_number,
                            anchor_style=None,
                            anchor_number=anchor_number,
                            anchor_type_number=anchor_type_number))

                    elif anchor_type_number == '2': # grouted tieback
                        anchor_parameters.append(AnchorParameterGroutedTieback(
                            anchor_name=anchor_number,
                            anchor_style=None,
                            anchor_number=anchor_number,
                            anchor_type_number=anchor_type_number))
                        
                    elif anchor_type_number == '4': # geo-textile
                        anchor_parameters.append(AnchorParameterGeoTextile(
                            anchor_name=anchor_number,
                            anchor_style=None,
                            anchor_number=anchor_number,
                            anchor_type_number=anchor_type_number)) 
                        
                    elif anchor_type_number == '5': # grouted tieback friction
                        anchor_parameters.append(AnchorParameterGroutedTiebackFriction(
                            anchor_name=anchor_number,
                            anchor_style=None,
                            anchor_number=anchor_number,
                            anchor_type_number=anchor_type_number))
                    
                    elif anchor_type_number == '6': # micro pile
                        anchor_parameters.append(AnchorParameterMicroPile(
                            anchor_name=anchor_number,
                            anchor_style=None,
                            anchor_number=anchor_number,
                            anchor_type_number=anchor_type_number))
                        
                    elif anchor_type_number == '3': # soil nail
                        anchor_parameters.append(AnchorParameterSoilNail(
                            anchor_name=anchor_number,
                            anchor_style=None,
                            anchor_number=anchor_number,
                            anchor_type_number=anchor_type_number))
                        
                        
                    j += 1
                    line = lines[j].strip()
                
                input_data.anchor_parameters = anchor_parameters



            elif line.startswith('material properties:'):
                j = i+1
                line = lines[j].strip()
                soil_styles_list = []
                support_styles_list = []
                
                while line != '':
                    name = line.split('    red:')[0]
                    data_color = line.split('    ')[-1].replace('  ',' ').split(' ')

                    # ['red:', '255', 'green:', '255', 'blue:', '193', 'hatch:', '2147483647']
                    color = Color(
                        red=int(data_color[1]),
                        green=int(data_color[3]),
                        blue=int(data_color[5])
                    )                    
                    if len(data_color) > 7:
                        hatch = data_color[7]
                        soil_styles_list.append([                            
                            name,
                            SoilStyle(color=color,hatch=hatch)
                        ])
                        
                    else:
                        support_styles_list.append([
                            name,
                            SupportStyle(
                                color=color
                            )
                        ])






                    j += 1
                    line = lines[j].strip()
                    

            i += 1
        

        # se agrega los item de la geometria
        input_data.geometry = Geometry(
            vertices=vertices,
            cells=cells,
            anchors=anchors,
            water_table=water_table,
            slope=slope,
            exterior=exterior,
            forces=forces,
            slope_limits=slope_limits
        )

        # se agrega los estilos a los parametros de suelo

        for soil in input_data.soil_parameters:
            soil_number= int(soil.soil_number.replace('soil', ''))
            soil.soil_name = soil_styles_list[soil_number-1][0]
            soil.soil_style = soil_styles_list[soil_number-1][1]

        # se agrega los estilos a los parametros de anclajes
        for anchor in input_data.anchor_parameters:
            anchor_number= int(anchor.anchor_number.replace('anchor', ''))
            anchor.anchor_name = support_styles_list[anchor_number-1][0]
            anchor.anchor_style = support_styles_list[anchor_number-1][1]    


        self._input_data = input_data


'''