# Implentación de JPA

## Entities

Lista de variables:
- Nombre Tabla
- Nombre Relacion
- Nombre Columna (Puede ser 1 o más)

Path:
```
NOMBRE_PROYECTO/NOMBRE_PROYECTO/src/main/java/com.example.NOMBRE_PROYECTO/entities/NombreTabla.java
// Considear tipo CLASS en la creación del archivo
```

Código:
```java
// ... imports

@Entity
@Table(name = "NombreTabla")
public class NombreTabla {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int idNombreTabla;
	
	// Cuando hay columna con dato String (El length es customizable)
    @Column(name = "nombreColumna", length = 50, nullable = false)
    private String nombreColumna;
	
	// Cuando hay columna con dato Double, Int o LocalDate
    @Column(name = "nombreColumna", nullable = false)
    private Double nombreColumna;
	
	// Cuando hay una relación de uno a muchos
    @ManyToOne
    @JoinColumn(name = "idNombreRelacion")
    private NombreRelacion nombreRelacion;

    // Generate > Constructor (Select none)
	// Generate > Constructor (Select all)
	// Generate > Getter and setter (Select all)
}
```

## Repository

Lista de variables:
- Nombre Tabla
- Nombre Columna (Puede ser 0 o más)
- Tipo Dato de Columna (Respecto a una columna NombreColumna)

Path:
```
NOMBRE_PROYECTO/NOMBRE_PROYECTO/src/main/java/com.example.NOMBRE_PROYECTO/repositories/INombreTablaRepository.java
// Considear tipo INTERFACE en la creación del archivo
```

Código:
```java
// ... imports

@Repository
public interface INombreTablaRepository extends JpaRepository<NombreTabla, Integer> {
	List<NombreTabla> findByNombreColumna(LocalDate nombreColumna); // (Date Filter) Retrieve all items by NombreColumna from table
}
```

## Service Interface

Lista de variables:
- Nombre Tabla
- Nombre Columna (Puede ser 0 o más)
- Tipo Dato de Columna (Respecto a una columna NombreColumna)

Path:
```
NOMBRE_PROYECTO/NOMBRE_PROYECTO/src/main/java/com.example.NOMBRE_PROYECTO/serviceinterfaces/INombreTablaService.java
// Considear tipo INTERFACE en la creación del archivo
```

Código:
```java
// ... imports
public interface INombreTablaService {
    void insert(NombreTabla nombreTabla); // Add an item to table
    
    void delete(int idNombreTabla); // Delete an item by ID on table
	
    NombreTabla listId(int idNombreTabla); // Retrieve an items by ID from table
    List<NombreTabla> findByNombreColumna(LocalDate nombreColumna); // (Date Filter) Retrieve all items by NombreColumna from table
	List<NombreTabla> list(); // Retrieve all items from table
}
```

## Service Implement

Lista de variables:
- Nombre Tabla
- Nombre Columna (Puede ser 0 o más)
- Tipo Dato de Columna (Respecto a una columna NombreColumna)

Path:
```
NOMBRE_PROYECTO/NOMBRE_PROYECTO/src/main/java/com.example.NOMBRE_PROYECTO/serviceimplements/NombreTablaServiceImplement.java
// Considear tipo CLASS en la creación del archivo
```

Código:
```java
// ... imports
@Service
public class NombreTablaServiceImplement implements INombreTablaService {
    @Autowired
    private INombreTablaRepository myRepository;
	
	// Add an item to table
    @Override
    public void insert(NombreTabla nombreTabla) {
        myRepository.save(nombreTabla);
    }

	// Delete an item by ID on table
	@Override
    public void delete(int idNombreTabla){
        myRepository.deleteById(idNombreTabla);
    }
	
	// Retrieve an items by ID from table
	@Override
    public NombreTabla listId(int idNombreTabla){
        return myRepository.findById(idNombreTabla).orElse(new NombreTabla());
    }
	
	// Retrieve all items from table
    @Override
    public List<NombreTabla> list() {
        return myRepository.findAll();
    }
	
	// (Date filter) Retrieve all items by NombreColumna from table
	@Override
    public List<NombreTabla> findByNombreColumna(LocalDate nombreColumna) {
        return myRepository.findByNombreColumna(nombreColumna);
    }
}
```

## DTOs

Lista de variables:
- Nombre Tabla
- Nombre Columna (Puede ser 0 o más)
- Tipo Dato de Columna (Respecto a una columna NombreColumna)
- Nombre Relación (Puede ser 0 o más)

Path:
```
NOMBRE_PROYECTO/NOMBRE_PROYECTO/src/main/java/com.example.NOMBRE_PROYECTO/dtos/NombreTablaDTO.java
// Considear tipo CLASS en la creación del archivo
```

Código:
```java
// ... imports
public class NombreTablaDTO {
	private int idNombreTabla;
	
	// Cuando hay columna con dato String
    private String nombreColumna;
	
	// Cuando hay columna con dato Double o Int
    private Double nombreColumna;
	
	// Cuando hay una relación de uno a muchos
    private NombreRelacion nombreRelacion;

	// Generate > Getter and setter (Select all)
}
```

## Controllers

Lista de variables:
- Nombre Tabla
- Nombre Columna (Puede ser 0 o más)
- Tipo Dato de Columna (Respecto a una columna NombreColumna)

Path:
```
NOMBRE_PROYECTO/NOMBRE_PROYECTO/src/main/java/com.example.NOMBRE_PROYECTO/controllers/NombreTablaController.java
// Considear tipo CLASS en la creación del archivo
```

Código:
```java
// ... imports
@RestController
@RequestMapping("/nombretabla")
public class NombreTablaController {
    @Autowired
    private INombreTablaService myService;
	
	// Add an item to table
    @PostMapping
    public void registrar(@RequestBody NombreTablaDTO dto) {
        ModelMapper m = new ModelMapper();
        NombreTabla myItem = m.map(dto, NombreTabla.class);
        myService.insert(myItem);
    }
	
	// Delete an item by ID on table
	@DeleteMapping("/{id}")
    public void eliminar(@PathVariable("id")Integer id){
        myService.delete(id);
    }
	
	// Retrieve an items by ID from table
	@GetMapping("/{id}")
    public NombreTablaDTO listarId(@PathVariable("id")Integer id){
        ModelMapper m = new ModelMapper();
        NombreTablaDTO myItem = m.map(myService.listId(id), NombreTablaDTO.class);
        return myItem;
    }
	
	// Retrieve all items from table
    @GetMapping
    public List<NombreTablaDTO> listar(){
        return myService.list().stream().map(x -> {
            ModelMapper m = new ModelMapper();
            return m.map(x, NombreTablaDTO.class);
        }).collect(Collectors.toList());
    }
    
	// (Exclusive to controller) Modify values on table
    @PutMapping
    public void modificar(@RequestBody NombreTablaDTO dto) {
        ModelMapper m = new ModelMapper();
        NombreTabla d = m.map(dto, NombreTabla.class);
        myService.insert(d);
    }
	
	// (Date Filter) Retrieve all items by NombreColumna from table
	@PostMapping("/buscar")
    public List<NombreTablaDTO> buscar(@RequestBody LocalDate nombreColumna){
        return myService.findByNombreColumna(nombreColumna).stream().map(x -> {
            ModelMapper m = new ModelMapper();
            return m.map(x, NombreTablaDTO.class);
        }).collect(Collectors.toList());
    }
}
```
