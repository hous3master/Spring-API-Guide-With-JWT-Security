import os

# Generates the entity file
def generateEntityFile(projectName, entityName, attributes):
    content = ''
    # Generate imports and package
    content += f'package pe.edu.upc.aaw.{projectName}.entities;\n\n'
    content += 'import javax.persistence.*;\n'
    content += f'import pe.edu.upc.aaw.{projectName}.entities.*;\n'
    content += 'import java.time.LocalDate;\n\n'

    content += f'@Entity\n@Table(name = \"{entityName.capitalize()}\")\npublic class {entityName.capitalize()} {{\n\n'
    content += '@Id\n'
    content += '@GeneratedValue(strategy = GenerationType.IDENTITY)\n'
    content += f'private int id{entityName.capitalize()};\n\n'
    for attribute in attributes:
        # if attribute is tipe LocalDate, int, double, String or boolean
        if attribute[0] == 'LocalDate' or attribute[0] == 'int' or attribute[0] == 'double' or attribute[0] == 'String' or attribute[0] == 'boolean':
            content += f'@Column(name = "{attribute[1]}", nullable = false)\n'
            content += f'private {attribute[0]} {attribute[1]};\n\n'

        # if attribute is a foreign key
        else:
            content += f'@ManyToOne\n'
            content += f'@JoinColumn(name = "id{attribute[1].capitalize()}")\n'
            content += f'private {attribute[0]} {attribute[1]};\n\n'
            
    # Generate empty constructor
    content += f'public {entityName.capitalize()}() {{ }}\n\n'

    # Generate constructor (for attributes, including ID)
    content += f'public {entityName.capitalize()}('
    content += f'int id{entityName.capitalize()},'
    for attribute in attributes:
        content += f'{attribute[0]} {attribute[1]}, '
    content = content[:-2]
    content += ') {\n'
    content += f'    this.id{entityName.capitalize()} = id{entityName.capitalize()};\n'
    for attribute in attributes:
        content += f'    this.{attribute[1]} = {attribute[1]};\n'
    content += '}\n\n'

    # Generate getters and setters (for attributes, including ID)
    # ID
    content += f'public int getId{entityName.capitalize()}() {{\n'
    content += f'    return id{entityName.capitalize()};\n'
    content += '}\n\n'
    content += f'public void setId{entityName.capitalize()}(int id{entityName.capitalize()}) {{\n'
    content += f'    this.id{entityName.capitalize()} = id{entityName.capitalize()};\n'
    content += '}\n\n'
    # Attributes
    for attribute in attributes:
        content += f'public {attribute[0]} get{attribute[1].capitalize()}() {{\n'
        content += f'    return {attribute[1]};\n'
        content += '}\n\n'
        content += f'public void set{attribute[1].capitalize()}({attribute[0]} {attribute[1]}) {{\n'
        content += f'    this.{attribute[1]} = {attribute[1]};\n'
        content += '}\n\n'
    content += '}'

    # Create a folder called ProjectName/Entities
    if not os.path.exists(f'{projectName}/entities'):
        os.makedirs(f'{projectName}/entities')

    # Create a txt file, write the data and close it. In a folder called ProjectName/Entities
    f = open(f'{projectName}/entities/{entityName.capitalize()}.java', 'w')
    f.write(content)    
    f.close()

# Generates the repository file
def generateRepositoryFile(projectName, entityName):
    content = ''
    # Generate imports and package
    content += f'package pe.edu.upc.aaw.{projectName}.repositories;\n\n'
    content += 'import org.springframework.data.jpa.repository.JpaRepository;\n'
    content += 'import org.springframework.stereotype.Repository;\n'
    content += f'import pe.edu.upc.aaw.{projectName}.entities.{entityName.capitalize()};\n'
    content += 'import java.util.List;\n\n'

    content += f'@Repository\npublic interface I{entityName.capitalize()}Repository extends JpaRepository<{entityName.capitalize()}, Integer> {{ }}'

    # Create a folder called ProjectName/Repositories
    if not os.path.exists(f'{projectName}/repositories'):
        os.makedirs(f'{projectName}/repositories')

    # Create a txt file, write the data and close it. In a folder called ProjectName/Repositories
    f = open(f'{projectName}/repositories/I{entityName.capitalize()}Repository.java', 'w')
    f.write(content)
    f.close()

# Generates the service interface file
def generateServiceInterface(projectName, entityName):
    content = ''
    # Generate imports and package
    content += f'package pe.edu.upc.aaw.{projectName}.serviceinterfaces;\n\n'
    content += f'import pe.edu.upc.aaw.{projectName}.entities.{entityName.capitalize()};\n'
    content += 'import java.util.List;\n\n'

    content += f'public interface I{entityName.capitalize()}Service {{\n'
    content += f'    void insert({entityName.capitalize()} {entityName});\n'
    content += f'    void delete(int id);\n'
    content += f'    {entityName.capitalize()} listId(int id);\n'
    content += f'    List<{entityName.capitalize()}> list();\n'
    content += '}'

    # Create a folder called ProjectName/serviceinterfaces
    if not os.path.exists(f'{projectName}/serviceinterfaces'):
        os.makedirs(f'{projectName}/serviceinterfaces')

    # Create a txt file, write the data and close it. In a folder called ProjectName/serviceinterfaces
    f = open(f'{projectName}/serviceinterfaces/I{entityName.capitalize()}Service.java', 'w')
    f.write(content)
    f.close()

# Generates the service implement file
def generateServiceImplement(projectName, entityName):
    content = ''
    # Generate imports and package
    content += f'package pe.edu.upc.aaw.{projectName}.serviceimplements;\n\n'
    content += 'import org.springframework.beans.factory.annotation.*;\n'
    content += 'import org.springframework.stereotype.*;\n'
    content += f'import pe.edu.upc.aaw.{projectName}.entities.{entityName.capitalize()};\n'
    content += f'import pe.edu.upc.aaw.{projectName}.repositories.I{entityName.capitalize()}Repository;\n'
    content += f'import pe.edu.upc.aaw.{projectName}.serviceinterfaces.I{entityName.capitalize()}Service;\n\n'

    content += 'import java.util.List;\n\n'

    content += f'@Service\npublic class {entityName.capitalize()}ServiceImplement implements I{entityName.capitalize()}Service {{\n'
    content += f'    @Autowired\n'
    content += f'    private I{entityName.capitalize()}Repository myRepository;\n\n'
    
    # Add an item to table
    content += f'    // Add an item to table\n'
    content += f'    @Override\n'
    content += f'    public void insert({entityName.capitalize()} {entityName}) {{\n'
    content += f'        myRepository.save({entityName});\n'
    content += f'    }}\n\n'

    # Delete an item by ID on table
    content += f'    // Delete an item by ID on table\n'
    content += f'    @Override\n'
    content += f'    public void delete(int id{entityName.capitalize()}){{\n'
    content += f'        myRepository.deleteById(id{entityName.capitalize()});\n'
    content += f'    }}\n\n'

    # Retrieve an items by ID from table
    content += f'    // Retrieve an items by ID from table\n'
    content += f'    @Override\n'
    content += f'    public {entityName.capitalize()} listId(int id{entityName.capitalize()}){{\n'
    content += f'        return myRepository.findById(id{entityName.capitalize()}).orElse(new {entityName.capitalize()}());\n'
    content += f'    }}\n\n'

    # Retrieve all items from table
    content += f'    // Retrieve all items from table\n'
    content += f'    @Override\n'
    content += f'    public List<{entityName.capitalize()}> list() {{\n'
    content += f'        return myRepository.findAll();\n'
    content += f'    }}\n'
    content += '}'

    # Create a folder called ProjectName/serviceimplements
    if not os.path.exists(f'{projectName}/serviceimplements'):
        os.makedirs(f'{projectName}/serviceimplements')

    # Create a txt file, write the data and close it. In a folder called ProjectName/serviceimplements
    f = open(f'{projectName}/serviceimplements/{entityName.capitalize()}ServiceImplement.java', 'w')
    f.write(content)
    f.close()

# Generates the DTO file
def generateDTO(projectName, entityName, attributes):
    content = ''
    # Generate imports and package
    content += f'package pe.edu.upc.aaw.{projectName}.dtos;\n\n'
    content += f'import pe.edu.upc.aaw.{projectName}.entities.*;\n'
    content += 'import java.time.LocalDate;\n\n'

    content += f'public class {entityName.capitalize()}DTO {{\n'

    # Generates id attribute
    content += f'    private int id{entityName.capitalize()};\n'

    # Generate attributes
    for attribute in attributes:
        content += f'    private {attribute[0]} {attribute[1]};\n'
    content += '\n'

    # Generate id attribute getter and setter
    content += f'    public int getId{entityName.capitalize()}() {{\n'
    content += f'        return id{entityName.capitalize()};\n'
    content += '    }\n\n'
    content += f'    public void setId{entityName.capitalize()}(int id{entityName.capitalize()}) {{\n'
    content += f'        this.id{entityName.capitalize()} = id{entityName.capitalize()};\n'
    content += '    }\n\n'

    # Generate attributes getters and setters
    for attribute in attributes:
        content += f'    public {attribute[0]} get{attribute[1].capitalize()}() {{\n'
        content += f'        return {attribute[1]};\n'
        content += '    }\n\n'
        content += f'    public void set{attribute[1].capitalize()}({attribute[0]} {attribute[1]}) {{\n'
        content += f'        this.{attribute[1]} = {attribute[1]};\n'
        content += '    }\n\n'
    content += '}'

    # Create a folder called ProjectName/dtos
    if not os.path.exists(f'{projectName}/dtos'):
        os.makedirs(f'{projectName}/dtos')

    # Create a txt file, write the data and close it. In a folder called ProjectName/dtos
    f = open(f'{projectName}/dtos/{entityName.capitalize()}DTO.java', 'w')
    f.write(content)
    f.close()

# Generates the controller file
def generateController(projectName, entityName):
    content = ''
    # Generate imports and package
    content += f'package pe.edu.upc.aaw.{projectName}.controllers;\n\n'
    content += 'import org.modelmapper.ModelMapper;\n'
    content += 'import org.springframework.beans.factory.annotation.Autowired;\n'
    content += 'import org.springframework.web.bind.annotation.*;\n'
    content += f'import pe.edu.upc.aaw.{projectName}.dtos.{entityName.capitalize()}DTO;\n'
    content += f'import pe.edu.upc.aaw.{projectName}.entities.{entityName.capitalize()};\n'
    content += f'import pe.edu.upc.aaw.{projectName}.serviceinterfaces.I{entityName.capitalize()}Service;\n\n'

    content += 'import java.util.List;\n'
    content += 'import java.util.stream.Collectors;\n\n'

    content += f'@RestController\n'
    content += f'@CrossOrigin(origins = "http://localhost:4200")\n'
    content += f'@RequestMapping("/{entityName.lower()}")\n'
    content += f'public class {entityName.capitalize()}Controller {{\n'
    content += f'    @Autowired\n'
    content += f'    private I{entityName.capitalize()}Service myService;\n\n'

    # Add an item to table
    content += f'    // Add an item to table\n'
    content += f'    @PostMapping\n'
    content += f'    public void registrar(@RequestBody {entityName.capitalize()}DTO dto) {{\n'
    content += f'        ModelMapper m = new ModelMapper();\n'
    content += f'        {entityName.capitalize()} myItem = m.map(dto, {entityName.capitalize()}.class);\n'
    content += f'        myService.insert(myItem);\n'
    content += f'    }}\n\n'

    # Delete an item by ID on table
    content += f'    // Delete an item by ID on table\n'
    content +=  '    @DeleteMapping("/{id}")\n'
    content += f'    public void eliminar(@PathVariable("id")Integer id){{\n'
    content += f'        myService.delete(id);\n'
    content += f'    }}\n\n'

    # Retrieve an items by ID from table
    content += f'    // Retrieve an items by ID from table\n'
    content +=  '    @GetMapping("/{id}")\n'

    content += f'    public {entityName.capitalize()}DTO listarId(@PathVariable("id")Integer id){{\n'
    content += f'        ModelMapper m = new ModelMapper();\n'
    content += f'        {entityName.capitalize()}DTO myItem = m.map(myService.listId(id), {entityName.capitalize()}DTO.class);\n'
    content += f'        return myItem;\n'
    content += f'    }}\n\n'

    # Retrieve all items from table
    content += f'    // Retrieve all items from table\n'
    content += f'    @GetMapping\n'
    content += f'    public List<{entityName.capitalize()}DTO> listar(){{\n'
    content += f'        return myService.list().stream().map(x -> {{\n'
    content += f'            ModelMapper m = new ModelMapper();\n'
    content += f'            return m.map(x, {entityName.capitalize()}DTO.class);\n'
    content += f'        }}).collect(Collectors.toList());\n'
    content += f'    }}\n\n'

    # (Exclusive to controller) Modify values on table
    content += f'    // (Exclusive to controller) Modify values on table\n'
    content += f'    @PutMapping\n'
    content += f'    public void modificar(@RequestBody {entityName.capitalize()}DTO dto) {{\n'
    content += f'        ModelMapper m = new ModelMapper();\n'
    content += f'        {entityName.capitalize()} d = m.map(dto, {entityName.capitalize()}.class);\n'
    content += f'        myService.insert(d);\n'
    content += f'    }}\n'
    content += '}'

    # Create a folder called ProjectName/controllers
    if not os.path.exists(f'{projectName}/controllers'):
        os.makedirs(f'{projectName}/controllers')

    # Create a txt file, write the data and close it. In a folder called ProjectName/controllers
    f = open(f'{projectName}/controllers/{entityName.capitalize()}Controller.java', 'w')
    f.write(content)
    f.close()

# Generates the CORS util
def generateUtilForCORS(projectName):
    """package pe.edu.upc.aaw.demo1_202302_si63.util;

    import java.io.IOException;

    import javax.servlet.Filter;
    import javax.servlet.FilterChain;
    import javax.servlet.FilterConfig;
    import javax.servlet.ServletException;
    import javax.servlet.ServletRequest;
    import javax.servlet.ServletResponse;
    import javax.servlet.http.HttpServletRequest;
    import javax.servlet.http.HttpServletResponse;

    import org.springframework.core.Ordered;
    import org.springframework.core.annotation.Order;
    import org.springframework.stereotype.Component;

    @Component
    @Order(Ordered.HIGHEST_PRECEDENCE)
    public class CORS implements Filter {

        @Override
        public void init(FilterConfig filterConfig) throws ServletException {
            // TODO Auto-generated method stub

        }

        @Override
        public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
                throws IOException, ServletException {
            HttpServletResponse response = (HttpServletResponse) res;
            HttpServletRequest request = (HttpServletRequest) req;

            response.setHeader("Access-Control-Allow-Origin", "*");
            response.setHeader("Access-Control-Allow-Methods", "DELETE, GET, OPTIONS, PATCH, POST, PUT");
            response.setHeader("Access-Control-Max-Age", "3600");
            response.setHeader("Access-Control-Allow-Headers",
                    "x-requested-with, authorization, Content-Type, Authorization, credential, X-XSRF-TOKEN");

            if ("OPTIONS".equalsIgnoreCase(request.getMethod())) {
                response.setStatus(HttpServletResponse.SC_OK);
            } else {
                chain.doFilter(req, res);
            }
            // chain.doFilter(req, res);
        }

        @Override
        public void destroy() {
            // TODO Auto-generated method stub
        }
    }"""
    content = ''
    # Generate package
    content += f'package pe.edu.upc.aaw.{projectName}.util;\n\n'
    # Generate imports
    content += 'import java.io.IOException;\n'
    content += 'import javax.servlet.Filter;\n'
    
    content += 'import javax.servlet.FilterChain;\n'
    content += 'import javax.servlet.FilterConfig;\n'
    content += 'import javax.servlet.ServletException;\n'
    content += 'import javax.servlet.ServletRequest;\n'
    content += 'import javax.servlet.ServletResponse;\n'
    content += 'import javax.servlet.http.HttpServletRequest;\n'
    content += 'import javax.servlet.http.HttpServletResponse;\n'
    content += 'import org.springframework.core.Ordered;\n'
    content += 'import org.springframework.core.annotation.Order;\n'
    content += 'import org.springframework.stereotype.Component;\n\n'

    content += '@Component\n'
    content += '@Order(Ordered.HIGHEST_PRECEDENCE)\n'
    content += 'public class CORS implements Filter {\n\n'

    content += '@Override\n'
    content += 'public void init(FilterConfig filterConfig) throws ServletException {\n'
    content += '    // TODO Auto-generated method stub\n\n'
    content += '}\n\n'
    
    content += '@Override\n'
    content += 'public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)\n'
    content += '        throws IOException, ServletException {\n'
    content += '    HttpServletResponse response = (HttpServletResponse) res;\n'
    content += '    HttpServletRequest request = (HttpServletRequest) req;\n\n'
    
    content += '    response.setHeader("Access-Control-Allow-Origin", "*");\n'
    content += '    response.setHeader("Access-Control-Allow-Methods", "DELETE, GET, OPTIONS, PATCH, POST, PUT");\n'
    content += '    response.setHeader("Access-Control-Max-Age", "3600");\n'
    content += '    response.setHeader("Access-Control-Allow-Headers",\n'
    content += '            "x-requested-with, authorization, Content-Type, Authorization, credential, X-XSRF-TOKEN");\n\n'

    content += '    if ("OPTIONS".equalsIgnoreCase(request.getMethod())) {\n'
    content += '        response.setStatus(HttpServletResponse.SC_OK);\n'
    content += '    } else {\n'
    content += '        chain.doFilter(req, res);\n'
    content += '    }\n'
    content += '    // chain.doFilter(req, res);\n'
    content += '}\n\n'

    content += '@Override\n'
    content += 'public void destroy() {\n'
    content += '    // TODO Auto-generated method stub\n'
    content += '}\n'
    content += '}'

    # Create a folder called ProjectName/util
    if not os.path.exists(f'{projectName}/util'):
        os.makedirs(f'{projectName}/util')

    # Create a txt file, write the data and close it. In a folder called ProjectName/util
    f = open(f'{projectName}/util/CORS.java', 'w')
    f.write(content)
    f.close()

# Generates all files for each entity
def generateAllFiles(projectName, entities):
    # Generate all files for each entityAlternativa
    for entity in entities:
        generateEntityFile(projectName, entity['entityName'], entity['attributes'])
        generateRepositoryFile(projectName, entity['entityName'])
        generateServiceInterface(projectName, entity['entityName'])
        generateServiceImplement(projectName, entity['entityName'])
        generateDTO(projectName, entity['entityName'], entity['attributes'])
        generateController(projectName, entity['entityName'])

    # Generate CORS util
    generateUtilForCORS(projectName)

projectName = 'aymaraacademiaapi'
entities = [
    {
        'entityName': 'Alternativa',
        'attributes': [
            ['String', 'respuesta'],
            ['boolean', 'correcta']
        ]
    },
    {
        'entityName': 'Estudiante',
        'attributes': [
            ['String', 'nombre'],
            ['String', 'apellido'],
            ['int', 'edad'],
            ['int', 'resena'],
            ['String', 'email'],
            ['Users', 'user'], # Many to one
        ]
    },
    {
        'entityName': 'Lectura',
        'attributes': [
            ['String', 'descripcion'],
            ['String', 'titulo'],
            ['String', 'autor'],
            ['Modulo', 'modulo'], # Many to one
        ]
    },
    {
        'entityName': 'Modulo',
        'attributes': [
            ['String', 'nombre'],
            ['String', 'descripcion']
        ]
    },
    {
        'entityName': 'Pregunta',
        'attributes': [
            ['String', 'pregunta'],
            ['Quizz', 'quizz'] # Many to one
        ]
    },
    {
        'entityName': 'Preguntaalternativa',
        'attributes': [
            ['Pregunta', 'pregunta'], # Many to one
            ['Alternativa', 'alternativa'], # Many to one
        ]
    },
    {
        'entityName': 'Progreso',
        'attributes': [
            ['double', 'progreso'],
            ['Estudiante', 'estudiante'], # Many to one
            ['Modulo', 'modulo'], # Many to one
        ]
    },
    {
        'entityName': 'Proyecto',
        'attributes': [
            ['String', 'titulo'],
            ['String', 'descripcion'],
            ['Unidad', 'unidad'], # Many to one
            ['double', 'calificacion'],
            ['int', 'contador'],
            ['Estudiante', 'estudiante'], # Many to one
        ]
    },
    {
        'entityName': 'Quizz',
        'attributes': [
            ['String', 'titulo'],
            ['Modulo', 'modulo'], # Many to one
        ]
    },
    { 'entityName': 'Role',
     
        'attributes': [
            ['String', 'rol'],
            ['Users', 'user'], # Many to one
        ]
    },
    {
        'entityName': 'Unidad',
        'attributes': [
            ['String', 'nombre'],
            ['String', 'descripcion'],
        ]
    },
    {
        'entityName': 'Unidadmodulo',
        'attributes': [
            ['Unidad', 'unidad'], # Many to one
            ['Modulo', 'modulo'], # Many to one
        ]
    },
    {
        'entityName': 'Users',
        'attributes': [
            ['String', 'username'],
            ['String', 'password'],
        ]
    },
    {
        'entityName': 'Video',
        'attributes': [

            ['String', 'url'],
            ['String', 'titulo'],
            ['String', 'descripcion'],
            ['double', 'duracion'],
            ['String', 'presentador'],
            ['String', 'transcripcion'],
            ['Modulo', 'modulo'], # Many to one
        ]
    },
    {
        'entityName': 'Cursounidad',
        'attributes': [
            ['Curso', 'curso'], # Many to one
            ['Unidad', 'unidad'], # Many to one
        ]
    },
    {
        'entityName': 'Curso',
        'attributes': [
            ['String', 'nombre'],
            ['String', 'descripcion']
        ]
    },
    {
        'entityName' : 'Estudiantepregunta',
        'attributes' : [
            ['Estudiante', 'estudiante'], # Many to one
            ['Pregunta', 'pregunta'], # Many to one
            ['boolean', 'correcta']
        ]
    },
    {
        'entityName' : 'Estudiantequizz',
        'attributes' : [
            ['Estudiante', 'estudiante'], # Many to one
            ['Quizz', 'quizz'], # Many to one
            ['double', 'calificacion']
        ]
    }
]

generateAllFiles(projectName, entities)