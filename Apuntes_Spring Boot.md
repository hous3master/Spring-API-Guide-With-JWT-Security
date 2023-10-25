# Setup del proyecto

## Creación del proyecto de Sprint Boot

En Add New Proyecto debemos ingresar la siguiente información

| Información | Valor asingnado |
| --- | --- |
| Name | nombreproyecto |
| Location | ~\Documents |
| Lnaguage | Java* |
| Type | Maven* |
| Group | pe.edu.upc.aaw |
| Artifact | nombreproyecto |
| Package name | pe.edu.upc.aaw.nombreproyecto |
| JDK | corretto-17* |
| Java | 17 |
| Packaging | War |

En la sección de depencias tenemos que **Spring Boot versión 2.7.14** y añadir:

- Spring Boot Dev Tools
- Spring Web
- Spring Data JPA
- PostgreSQL Driver

## Jerarquías

En *./src/main/java/pe.edu.upc.aaw.nombreproyecto*, debemos crear un **new package** con los siguientes nombres:

1. entities
2. repositories
3. serviceinterfaces
4. serviceimplements
5. dtos
6. controllers

## Base de datos

Antes de programar, debemos crear la base de datos, para ello seguiremos los siguientes pasos:

1. Entramos a pgAdmin4
2. Expandimos PostgreSQL 15 > Databases
3. Click derecho en Databases
4. Click izquierdo en Create Database
5. Ingresamos el nombre_base_de_datos en el campo Name
6. Click izquierdo en Save

## Propiedades de la aplicación

En *./src/main/java/resources/application.propieties* implementamos las siguientes propiedades para la conección a la base de datos:
```
spring.jpa.database=postgresql
spring.jpa.show-sql=false
spring.jpa.hibernate.ddl-auto=update
spring.datasource.driver-class-name=org.postgresql.Driver
spring.datasource.url=jdbc:postgresql://localhost/NOMBRE_DB
spring.datasource.username=postgres
spring.datasource.password=12345678
server.port=8080
```

## Dependencias

En ./pom.xml se deben inyectar las dependencias springdoc y modelmapper. Ambas mediante el siguiente código:

```
<!-- https://mvnrepository.com/artifact/org.springdoc/springdoc-openapi-ui -->
<dependency>
	<groupId>org.springdoc</groupId>
	<artifactId>springdoc-openapi-ui</artifactId>
	<version>1.6.4</version>
</dependency>


<!-- https://mvnrepository.com/artifact/org.modelmapper/modelmapper -->
<dependency>
	<groupId>org.modelmapper</groupId>
	<artifactId>modelmapper</artifactId>
	<version>3.1.1</version>
</dependency>
```

Tras añadir las dependencias debemos ir al panel Maven (ubicado en la barra lateral derecha) y dar click en *Reload Maven Project*