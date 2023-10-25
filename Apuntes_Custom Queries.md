# SQL en JPA

## Queries fijas

### Repository

###### Lista de variables
- MY QUERY
- functionality
- NombreTabla

###### Código
```java
@Query(value = "MY QUERY", nativeQuery = true)
public List<String[]> functionalityByNombreTabla();
```

### Service Interface

###### Lista de variables
- functionality
- NombreTabla

###### Código
```java
public List<String[]> functionalityByNombreTabla();
```

### Service Implement

###### Lista de variables
- functionality
- NombreTabla

###### Código
```java
@Override
public List<String[]> functionalityByNombreTabla() {
	return myRepository.functionalityByNombreTabla();
}
```

### Controller

###### Lista de variables
- functionality
- funcionalidad
- NombreTabla
- NombreColumna (1 a mas) <- es la columna del DTO
- nColumna <- Orden de columna de output query

###### Código
```java
@GetMapping("/cantidades")
public List<NombreTablaDTO> funcionalidadPorNombreTabla(){
	List<String[]> myList = myService.functionalityByNombreTabla();
	List<NombreTablaDTO> myListDTO = new ArrayList<>();
	for (String[] data:myList) {
		NombreTablaDTO dto = new NombreTablaDTO();
		dto.setNombreColumna(data[nColumna]); // Si es String
		dto.setNombreColumna(Integer.parseInt(data[nColumna])); // Si es Integer
		dto.setNombreColumna(Double.parseDouble(data[nColumna])); // Si es Double
		myListDTO.add(dto);
	}
	return myListDTO;
}
```
## Querys dinamicas

#### Repository

##### Lista de variables
- Nombre Tabla
- Columa Filtro
##### Código
###### Si el filtro es de tipo String
```java
@Query(value = "SELECT * FROM nombre_tabla WHERE columna_filtro = :name", nativeQuery = true)
public List<String[]> findNombreTablaByColumnaFiltro(@Param("name") String name);
```
###### Si el filtro es de tipo int
```java
@Query(value = "SELECT * FROM nombre_tabla WHERE columna_filtro = :name", nativeQuery = true)
public List<String[]> findNombreTablaByColumnaFiltro(@Param("name") int moduloId);
```

#### Service Interface

##### Lista de variables
- NombreTabla
- ColumnaFiltro

##### Código
###### Si el parámetro de búsqueda es String
```java
List<String[]> findNombreTablaByColumnaFiltro(String name);
```
###### Si el parámetro de búsqueda es int
```java
List<String[]> findNombreTablaByColumnaFiltro(int name);
```
#### Service Implement

##### Lista de variables
- Nombre Tabla
- Columna Filtro

##### Código
###### Si el parámetro de búsqueda es String
```java
@Override
public List<String[]> findNombreTablaByColumnaFiltro(String name) {
    return myRepository.findNombreTablaByColumnaFiltro(name);
}
```
###### Si el parámetro de búsqueda es int
```java
@Override
public List<String[]> findNombreTablaByColumnaFiltro(int name) {
    return myRepository.findNombreTablaByColumnaFiltro(name);
}
```
#### Controller

##### Lista de variables
- Nombre Tabla
- Columna Filtro
- Nombre Tabla DTO
- Name
###### Código
**Información en el body (POST)**
***Si el parámetro de búsqueda es String***
```java
@PostMapping("/buscar")
public List<NombreTablaDTO> nombreTablaByColumnaFiltro(@RequestBody String name) {
    List<String[]> myList = myService.findNombreTablaByColumnaFiltro(name);
    List<NombreTablaDTO> myListDTO = new ArrayList<>();
    for (String[] data:myList) {
        NombreTablaDTO dto = new NombreTablaDTO();
		
        dto.setNombreColumna(data[nColumna]); // Si es String
		dto.setNombreColumna(Integer.parseInt(data[nColumna])); // Si es Integer
		dto.setNombreColumna(Double.parseDouble(data[nColumna])); // Si es Double

        myListDTO.add(dto);
    }
    return myListDTO;
}
```
***Si el parámetro de búsqueda es int***
```java
@PostMapping("/buscar")
public List<NombreTablaDTO> nombreTablaByColumnaFiltro(@RequestBody int name) {
    List<String[]> myList = myService.findNombreTablaByColumnaFiltro(name);
    List<NombreTablaDTO> myListDTO = new ArrayList<>();
    for (String[] data:myList) {
        NombreTablaDTO dto = new NombreTablaDTO();
		
        dto.setNombreColumna(data[nColumna]); // Si es String
		dto.setNombreColumna(Integer.parseInt(data[nColumna])); // Si es Integer
		dto.setNombreColumna(Double.parseDouble(data[nColumna])); // Si es Double

        myListDTO.add(dto);
    }
    return myListDTO;
}
```
**Información en el path (GET)**
***Si el parámetro de búsqueda es String***
```java
@GetMapping("/buscar/{name}")
public List<NombreTablaDTO> nombreTablaByColumnaFiltro(@PathVariable("name") String name) {
	List<String[]> myList = myService.findNombreTablaByColumnaFiltro(name);
	List<NombreTablaDTO> myListDTO = new ArrayList<>();
	for (String[] data:myList) {
		NombreTablaDTO dto = new NombreTablaDTO();
		
        dto.setNombreColumna(data[nColumna]); // Si es String
		dto.setNombreColumna(Integer.parseInt(data[nColumna])); // Si es Integer
		dto.setNombreColumna(Double.parseDouble(data[nColumna])); // Si es Double

        myListDTO.add(dto);
	}
	return myListDTO;
}
```
***Si el parámetro de búsqueda es int***
```java
@GetMapping("/buscar/{name}")
public List<NombreTablaDTO> nombreTablaByColumnaFiltro(@PathVariable("name") int name) {
	List<String[]> myList = myService.findNombreTablaByColumnaFiltro(name);
	List<NombreTablaDTO> myListDTO = new ArrayList<>();
	for (String[] data:myList) {
		NombreTablaDTO dto = new NombreTablaDTO();
		
        dto.setNombreColumna(data[nColumna]); // Si es String
		dto.setNombreColumna(Integer.parseInt(data[nColumna])); // Si es Integer
		dto.setNombreColumna(Double.parseDouble(data[nColumna])); // Si es Double

        myListDTO.add(dto);
	}
	return myListDTO;
}
```

## Queries de ejemplo

Contar repeticiones

```sql
SELECT
	o.name_origen,
	COUNT (o.id_origen)
FROM origen o
INNER JOIN destino d ON o.id_origen = d.id_destino
GROUP BY o.name_origen
```

###### Sumar repeticiones

```sql
SELECT
	o.name_origen,
	SUM (d.amount_destino)
FROM origen o 
NNER JOIN destino d ON o.id_origen = d.id_destino
GROUP BY o.name_origen
```

###### Filtrar por campo foráneo
Cabe destacar que queries como estos requieren la creación de un nuevo DTO para poder pasar el ID como Integer.

```sql
SELECT
	d.id_destino,
	d.name_destino,
	d.quantity_destino,
	d.id_origen
FROM destino d
INNER JOIN origen o ON d.id_origen = o.id_origen
WHERE o.category_origen = :name
```
###### Contar B por categoria de A
```sql
SELECT
	o.category_origen,
	COUNT (d.id_destino)
FROM origen o
INNER JOIN destino d ON o.id_origen = d.id_destino
GROUP BY o.category_origen
```