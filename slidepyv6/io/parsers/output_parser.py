# io/file_handlers/output_parser.py
'''
from ...models.models_output import (
    SlideOutputData, GlobalMinimum, Surface, Grid, Point
)
from ...utils.exceptions import SlideError
'''
from ...models.results import ProjectResults
from ...models.results import GlobalMinimum, Surface,  Point, Method, EquilibriumTerms

import re

def isNumeric(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

class OutputParser:
    @staticmethod
    def parse(content: str) -> ProjectResults:

        # Si 'content' es bytes, decodificamos a string
        if isinstance(content, bytes):
            content = content.decode('utf-8', errors='ignore')
        

        # Bloque de información general
        #--------------------------------
        pattern_inf  = r"(?ms)(\* Version.*?)(?=\* Three Point Surfaces.*?|\* grid#.*?)"
        match_inf = next(re.finditer(pattern_inf, content, re.MULTILINE), None)
        block_inf = match_inf.group(1).strip() 
  
        # Bloque de superficies
        #--------------------------------
        # Definir patrón para el bloque que inicia con "* grid#"
        pattern_grid = r"(?ms)(\* grid#.*?)(?=\* Global Minimum FS \(xc,yc,r,x1,y1,x2,y2,fs,name\))"
        # Definir patrón para el bloque que inicia con "* Three Point Surfaces (xc,yc,r,yleft,x1,y1,x2,y2,yright,fs1,fs2,...,b1)"
        pattern_three  = r"(?ms)(\* Three Point Surfaces.*?)(?=\* Global Minimum FS \(xc,yc,r,x1,y1,x2,y2,fs,name\))"

        match_grid = next(re.finditer(pattern_grid, content, re.MULTILINE), None)
        match_three = next(re.finditer(pattern_three, content, re.MULTILINE), None)

    
        if match_grid :
            block_surface = match_grid.group(1).strip()
        elif match_three:
            block_surface = match_three.group(1).strip()
        else:
            block_surface = None

        # Bloque de mínimos globales
        #--------------------------------
        pattern_min  = r"(?ms)(\* Global Minimum FS.*?)(?=\* #data)"
        match_min = next(re.finditer(pattern_min, content, re.MULTILINE), None)
        block_min = match_min.group(1).strip()

  

        # Bloque de resultados de dobelas
        #--------------------------------
        pattern_data  = r"(?ms)(\* #data.*?)(?=\* bolt data \(#bolts,nummethods\))"
        match_data = next(re.finditer(pattern_data, content, re.MULTILINE), None)
        block_data = match_data.group(1).strip() 

        methods = OutputParser._parse_project_results_methods(block_inf)
        surfaces = OutputParser._parse_project_results_surfaces(block_surface, methods)        
        global_minimums = OutputParser._parse_project_results_global_minimums(block_min, block_data)

        project_results = ProjectResults(
            methods = methods,
            surfaces = surfaces,
            global_minimums = global_minimums
            
        )

        return project_results

    def _parse_project_results_methods( content: str) -> list[Method]:
        pattern = r"(?ms)^\*\s*(?P<key>.*?)\s*\n(?P<value>.*?)(?=^\*\s|\Z)"
        matches = re.finditer(pattern, content)
        data = {match.group("key"): match.group("value").strip() for match in matches}
        list_methods = []
        lines = data['Analysis names'].split('\n')
        i = 0
        for line in lines:
            name =line
            id_method = i
            list_methods.append(Method(id=id_method,name=name))
            i += 1
        return list_methods
       


    def _parse_project_results_surfaces( content: str, methods: list[Method]) -> list[Surface]:
        # [Method(id=0, name='ordinary/fellenius'), Method(id=1, name='bishop simplified'), Method(id=2, name='janbu simplified'), Method(id=3, name='janbu corrected'), Method(id=4, name='spencer'), Method(id=5, name='corp of eng#1'), Method(id=6, name='corp of eng#2'), Method(id=7, name='lowe-karafiath'), Method(id=8, name='gle/morgenstern-price')]
        methods = {method.id: method.name for method in methods}
        lines = content.split('\n')

        # Eliminar el primer  y ultimo caracter
        surfaces = []

        if lines[0] == '* grid#':
            grid_pattern = r"(?ms)(\* grid#.*?)(?=^\* grid#|\Z)"
            grid_blocks = [m.group(1).strip() for m in re.finditer(grid_pattern, content, re.MULTILINE)]
            sub_pattern = r"(?ms)(^\d+\.\d+\s+\d+\.\d+\s+\d+)(.*?)(?=^\d+\.\d+\s+\d+\.\d+\s+\d+|\Z)"

            for grid in grid_blocks:
           
                # Separamos los sub-bloques dentro del bloque actual:
                sub_blocks = [ (m.group(1).strip(), m.group(2).strip()) 
                            for m in re.finditer(sub_pattern, grid, re.MULTILINE) ]
                for header, data in sub_blocks:
                    line_header = header.split()
                    xc = float(line_header[0])
                    yc = float(line_header[1])
                    num_surfaces = int(line_header[2])
                    lines_data = data.split('\n')          
                    for line_data in lines_data:
                        parts = line_data.split()
                        # r,yleft,x1,y1,x2,y2,yright,fs...,b1
                        # ['21.1305931732312', '24.4612970394305', '3.73726738850118', '24.4612970394305', '38.5636419572064', '8.56150693891891', '8.56150693891891', '-112', '2.38275', '0.5']

                        i= 0
                        for j in range(7, len(parts)-1):
                            fs = float(parts[j])
                            method = methods[i]
                            surfaces.append(Surface(
                                method=method,
                                radius=float(parts[0]),
                                point1=Point(x=float(parts[2]), y=float(parts[3])),
                                point2=Point(x=float(parts[4]), y=float(parts[5])),
                                yleft=float(parts[1]),
                                yright=float(parts[6]),
                                fs=fs,
                                point_center=Point(x=xc, y=yc),
                                b1=parts[-1]
                            ))        
                            i += 1

            
        else:
            
            lines = lines[1:-1]
            for line in lines:
                parts = line.split() 
                i = 0                         
                for j in range(9, len(parts)-1):
                    fs =float(parts[j])  
                    method = methods[i]
                    # xc,yc,r,yleft,x1,y1,x2,y2,yright,fs1,fs2,...,b1
                    #['17.1625788950337', '23.5833231810127', '9.06919676514904', '23.5833231810127', '8.09338212988462', '23.5833231810127', '15.9247173995278', '14.5990018998622', '14.5990018998622', '1.85461', '1.82308', '0.5']
                    surfaces.append(Surface(
                        method=method,
                        radius=parts[2],
                        point1=Point(x=parts[4], y=parts[5]),
                        point2=Point(x=parts[6], y=parts[7]),
                        yleft=parts[3],
                        yright=parts[8],
                        fs=fs,
                        point_center=Point(x=parts[0], y=parts[1]),
                        b1=parts[-1]
                    ))
                    i += 1

        return surfaces


    def _parse_project_results_global_minimums( content_min: str, content_data: str) -> list[GlobalMinimum]:                                             
        pattern = r"(?ms)^\*\s*(?P<key>.*?)\s*\n(?P<value>.*?)(?=^\*\s|\Z)"
        matches = re.finditer(pattern, content_min)
        data = {match.group("key"): match.group("value").strip() for match in matches}
        list_global_minimums = []

        # procesamos la información de los mínimos globales → text
        # ---------------------------------------------------------
        lines_text = data['Global Minimum Text']
        blocks = re.split(r"^\s*\d+\s*$", lines_text, flags=re.MULTILINE)
        blocks = [b.strip() for b in blocks if b.strip()]
        pattern = r"^(Resisting Moment|Driving Moment|Resisting Horizontal Force|Driving Horizontal Force)=(\d+(?:\.\d+)?)"
        results_text = []
        for block in blocks:
            pairs = re.findall(pattern, block, flags=re.MULTILINE)
            # Inicializamos todas las claves a None
            d = {
                "Resisting Moment": None,
                "Driving Moment": None,
                "Resisting Horizontal Force": None,
                "Driving Horizontal Force": None
            }
            for key, value in pairs:
                d[key] = float(value)
            results_text.append(d)


        # procesamos la información de los mínimos globales → fs
        # ---------------------------------------------------------
        lines_fs = data['Global Minimum FS (xc,yc,r,x1,y1,x2,y2,fs,name)'].split('\n')
        for i, line in enumerate(lines_fs):

            # 1.
            parts = line.split()       
            method = ' '.join(parts[8:]) 
            
            # 2.
            surface = Surface( 
                method=method,
                radius=float(parts[2]),
                point1=Point(x=float(parts[3]), y=float(parts[4])),
                point2=Point(x=float(parts[5]), y=float(parts[6])),
                yleft=None,
                yright=None,
                fs = float(parts[7]),
                point_center=Point(x=float(parts[0]), y=float(parts[1])),
                b1=None
            )
            
            # 3.
            resisting_moment = results_text[i]["Resisting Moment"]
            driving_moment = results_text[i]["Driving Moment"]
            resisting_force = results_text[i]["Resisting Horizontal Force"]
            driving_force = results_text[i]["Driving Horizontal Force"]

            equilibriums =  EquilibriumTerms(
                resisting_moment=resisting_moment,
                driving_moment=driving_moment,
                resisting_force=resisting_force,
                driving_force=driving_force
            )

            # 4.
   
            list_global_minimums.append(GlobalMinimum(    
                surface=surface,
                equilibrium_terms=equilibriums
            ))
                    
        return list_global_minimums


        '''
        class GlobalMinimum:
            method: str
            surface: Surface
            resisting_moment: float | None
            driving_moment: float | None
            resisting_force: float | None
            driving_force: float | None
            slices: list[Slice]

        @dataclass
        class Surface:
            radius: float 
            point1: Point
            point2: Point
            yleft: float 
            yright: float 
            fs: list[float] 
            point_center: Point
            
            # revisar si es necesario
            b1: float

        @dataclass
        class Slice:
            x: float
            yt: float
            yb: float
            loc: int
            frictional_strength: float
            cohesive_strength: float
            base_normal_force: float
            base_friction_angle: float
            interslice_normal_force: float
            interslice_shear_force: float
            slice_weight: float
            pore_pressure: float
            m_alpha: float
            thrust_line_elevation: float
            initial_pore_pressure: float
            horizontal_seismic_force: float
            vertical_seismic_force: float
            phib: float
            base_cohesion: float
            base_material: str
        '''
            
        return global_minimums
        


'''

    @staticmethod
    def _parse_global_minimums(lines: list) -> list[GlobalMinimum]:
        # Lógica específica para mínimos
        return [GlobalMinimum(...), ...]
    


    def _parse_output_file(self) -> None:
        """Parsea el archivo de resultados (output)"""
        try:        
            output_content = self._io.read_project_file('output')
            lines = output_content.splitlines()

            output_data = SlideOutputData(
                version="",
                nun_grids=0,
                nun_analysis_types=0,
                analysis_names=[],
                surfaces=[],
                grids_results_fs=[],
                global_minimums_fs=[],
                analysis_results=[],
                minimum_surfaces=[]
            )
            i = 0
      
            
            while i < len(lines):
                line = lines[i].strip()
                

                # Parsear versión
                if line.startswith('* Version'):
                    i += 1 # saltar linea
                    line = lines[i].strip()
                    output_data.version = line

                # Parsear numero de grillas
                elif line.startswith('* #grids'):
                    i += 1 # saltar linea
                    line = lines[i].strip()
                    output_data.nun_grids = int(line)
                
                # Parsear numero de tipos de análisis
                elif line.startswith('* Number of analysis types'):
                    i += 1 # saltar linea
                    line = lines[i].strip()
                    output_data.nun_analysis_types = int(line)

                # Parsear tipos de análisis
                elif line.startswith('* Analysis names'):
                    i += 1                    
                    while i < len(lines) and not lines[i].startswith('*'):
                        output_data.analysis_names.append(lines[i].strip())
                        i += 1
                    continue

                # parsear los reusltados de las grillas
                elif line.startswith('* grid#'):

                    # leer el numero de grid
                    i += 1 
                    nun_grid = int(lines[i].strip())

                    # Leer nx ny
                    i += 2
                    nx_ny = lines[i].strip().split()
                    nx = int(nx_ny[0])
                    ny = int(nx_ny[1])
                    
                    # leer los puntos
                    i +=3
                    nun_points = (nx+1)*(ny+1)
                    points = []                    
                    for pj in range(nun_points):
                        data_point = lines[i].strip().split()
                        xc = float(data_point[0])
                        yc = float(data_point[1])
                        nun_surfaces = int(data_point[2])
                       
                        
                        surfaces = []
                        for _ in range(nun_surfaces):
                            i += 1
                            line = lines[i].strip()
                            parts = line.split()
                            fs=[]
                            for j in range(7, 7+output_data.nun_analysis_types):
                                fs.append(float(parts[j]))
                            surface = Surface(
                                r = float(parts[0]),
                                yleft = float(parts[1]),
                                x1 = float(parts[2]),
                                y1 = float(parts[3]),
                                x2 = float(parts[4]),
                                y2 = float(parts[5]),
                                yright = float(parts[6]),
                                fs= fs,
                                b1=float(parts[-1])
                            )                           

                            surfaces.append(surface)
                        # agregar el punto a la lista
                        points.append(Point(
                            xc=xc,
                            yc=yc,
                            nun_surfaces=nun_surfaces,
                            surfaces=surfaces
                        ))
                        i += 1

                    # Agregar grid a la lista de resultados
                    grid_result = Grid(
                        nun_grid=nun_grid,
                        nx=nx,
                        ny=ny,
                        points=points
                        
                    )
                    output_data.grids_results_fs.append(grid_result)                    

                elif line.startswith('* Three Point Surfaces'):
                    # (xc,yc,r,yleft,x1,y1,x2,y2,yright,fs1,fs2,...,b1)

                    i += 1

                    while i < len(lines) and not lines[i].startswith('$end'):
                        line = lines[i].strip()
                        parts = line.split()
                        fs = []
                        for j in range(9, len(parts)):
                            fs.append(float(parts[j]))
                        surface = Surface(
                            xc=float(parts[0]),
                            yc=float(parts[1]),
                            r=float(parts[2]),
                            yleft=float(parts[3]),
                            x1=float(parts[4]),
                            y1=float(parts[5]),
                            x2=float(parts[6]),
                            y2=float(parts[7]),
                            yright=float(parts[8]),
                            fs=fs,
                            b1=float(parts[-1])
                        )

                        # agregar la superficie a la lista
                        output_data.surfaces.append(surface)

                        i += 1
                    


                    continue
                    
   
          
                    points = []                    
                    for pj in range(nun_points):
                        data_point = lines[i].strip().split()
                        xc = float(data_point[0])
                        yc = float(data_point[1])
                        nun_surfaces = int(data_point[2])
                       
                        
                        surfaces = []
                        for _ in range(nun_surfaces):
                            i += 1
                            line = lines[i].strip()
                            parts = line.split()
                            fs=[]
                            for j in range(7, 7+output_data.nun_analysis_types):
                                fs.append(float(parts[j]))
                            surface = Surface(
                                r = float(parts[0]),
                                yleft = float(parts[1]),
                                x1 = float(parts[2]),
                                y1 = float(parts[3]),
                                x2 = float(parts[4]),
                                y2 = float(parts[5]),
                                yright = float(parts[6]),
                                fs= fs,
                                b1=float(parts[-1])
                            )                           

                            surfaces.append(surface)
                        # agregar el punto a la lista
                        points.append(Point(
                            xc=xc,
                            yc=yc,
                            nun_surfaces=nun_surfaces,
                            surfaces=surfaces
                        ))
                        i += 1

                    # Agregar grid a la lista de resultados
                    grid_result = Grid(
                        nun_grid=nun_grid,
                        nx=nx,
                        ny=ny,
                        points=points
                        
                    )
                    output_data.grids_results_fs.append(grid_result)                    



                # Parsear mínimos globales FS
                elif line.startswith('* Global Minimum FS'):
                    i += 1

                    while i < len(lines) and not lines[i].startswith('*'):
                        line = lines[i].strip()
                        parts = line.split()

                        # metodos dese el 7 hasta el final
                        methods = ''
                        for j in range(8, len(parts)):
                            methods += parts[j] + ' '

                        output_data.global_minimums_fs.append(
                            GlobalMinimum(
                                xc=float(parts[0]),
                                yc=float(parts[1]),
                                r=float(parts[2]),
                                x1=float(parts[3]),
                                y1=float(parts[4]),
                                x2=float(parts[5]),
                                y2=float(parts[6]),
                                fs=float(parts[7]),
                                method=methods
                            )
                        )
                        i += 1
                    continue
                    
                # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
                # aca falta la aprte de reusltados de las dobelas 
                # desde aca '* #data' hasta el final
                # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
                i += 1
                
            self._output_data = output_data
        
        

        except Exception as e:
            raise SlideError(f"Error al parsear el archivo de resultados: {e}") from e
        

        except Exception as e:
            raise SlideError(f"Error al leer el archivo de resultados: {e}") from e
        
'''