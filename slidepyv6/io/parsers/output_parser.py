
from ...models.results import ProjectResults
from ...models.results import GlobalMinimum, Surface,  Point, Method, EquilibriumTerms
import re

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
     