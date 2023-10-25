 ## Jerarquías

En *./src/main/java/pe.edu.upc.aaw.nombreproyecto*, debemos crear un **new package** con el nombre:
- security

## Propiedades de la aplicación

Se debe añadir el siguiente contenido a application.properties

Lista de variables:
- **nombre_database**
- **contrasena**

Código:
```java
spring.jackson.serialization.write-dates-as-timestamps=false
spring.jpa.properties.hibernate.jdbc.lob.non_contextual_creation=true
jwt.secret=4t7w!z%C*F-JaNdRgUkXn2r5u8x/A?D(G+KbPeShVmYq3s6v9y$B&E)H@McQfTjW
spring.devtools.restart.log-condition-evaluation-delta=false
```

## Dependencias

Se deben añadir las siguientes dependencias a pom.xml y recargar el proyecto Maven:
```xml
<dependency>
	<groupId>io.jsonwebtoken</groupId>
	<artifactId>jjwt</artifactId>
	<version>0.9.1</version>
</dependency>

<dependency>
	<groupId>org.glassfish.jaxb</groupId>
	<artifactId>jaxb-runtime</artifactId>
</dependency>

<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-starter-security</artifactId>
</dependency>
```

## Nuevos archivos
### Security

### JwtAuthenticationEntryPoint

```java
@Component
public class JwtAuthenticationEntryPoint implements AuthenticationEntryPoint, Serializable {

    private static final long serialVersionUID = -7858869558953243875L;

    @Override
    public void commence(HttpServletRequest request, HttpServletResponse response,
                         AuthenticationException authException) throws IOException {

        response.sendError(HttpServletResponse.SC_UNAUTHORIZED, "Unauthorized");
    }
}
```

### JwtRequest

```java
public class JwtRequest implements Serializable {
	private static final long serialVersionUID = 5926468583005150707L;
	private String username;
	private String password;
	public JwtRequest() {
		super();
		// TODO Auto-generated constructor stub
	}
	public JwtRequest(String username, String password) {
		super();
		this.username = username;
		this.password = password;
	}
	public static long getSerialversionuid() {
		return serialVersionUID;
	}
	public String getUsername() {
		return username;
	}
	public String getPassword() {
		return password;
	}
	public void setUsername(String username) {
		this.username = username;
	}
	public void setPassword(String password) {
		this.password = password;
	}
}
```

### JwtRequestFilter

```java
@Component
public class JwtRequestFilter extends OncePerRequestFilter {
	@Autowired
	private JwtUserDetailsService jwtUserDetailsService;
	@Autowired
	private JwtTokenUtil jwtTokenUtil;
	@Override
	protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain chain)
			throws ServletException, IOException {
		final String requestTokenHeader = request.getHeader("Authorization");
		String username = null;
		String jwtToken = null;
		// JWT Token is in the form "Bearer token". Remove Bearer word and get
		// only the Token
		if (requestTokenHeader != null && requestTokenHeader.startsWith("Bearer ")) {
			//jwtToken = requestTokenHeader.substring(7);
			jwtToken = requestTokenHeader.split(" ")[1].trim();

			try {
				username = jwtTokenUtil.getUsernameFromToken(jwtToken);
			} catch (IllegalArgumentException e) {
				System.out.println("No se puede encontrar el token JWT");
			} catch (ExpiredJwtException e) {
				System.out.println("Token JWT ha expirado");
			}
		} else {
			logger.warn("JWT Token no inicia con la palabra Bearer");
		}

		// Once we get the token validate it.
		if (username != null && SecurityContextHolder.getContext().getAuthentication() == null) {

			UserDetails userDetails = this.jwtUserDetailsService.loadUserByUsername(username);

			// if token is valid configure Spring Security to manually set
			// authentication
			if (jwtTokenUtil.validateToken(jwtToken, userDetails)) {

				UsernamePasswordAuthenticationToken usernamePasswordAuthenticationToken = new UsernamePasswordAuthenticationToken(
						userDetails, null, userDetails.getAuthorities());
				usernamePasswordAuthenticationToken
						.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));
				// After setting the Authentication in the context, we specify
				// that the current user is authenticated. So it passes the
				// Spring Security Configurations successfully.
				SecurityContextHolder.getContext().setAuthentication(usernamePasswordAuthenticationToken);
			}
		}
		chain.doFilter(request, response);
	}
}
```

### JwtResponse

```
public class JwtResponse implements Serializable {

	private static final long serialVersionUID = -8091879091924046844L;
	private final String jwttoken;

	public String getJwttoken() {
		return jwttoken;
	}

	public JwtResponse(String jwttoken) {
		super();
		this.jwttoken = jwttoken;
	}

}
```

### JwtTokenUtil

```java
@Component
public class JwtTokenUtil implements Serializable {

    private static final long serialVersionUID = -2550185165626007488L;

    //milisegundos || 18 minutos, le quitamos mil 18 segundos demo
    public static final long JWT_TOKEN_VALIDITY = 7 * 60 * 60 * 1000;

    @Value("${jwt.secret}")
    private String secret;

    //retrieve username from jwt token
    public String getUsernameFromToken(String token) {
        return getClaimFromToken(token, Claims::getSubject);
    }

    //retrieve expiration date from jwt token
    public Date getExpirationDateFromToken(String token) {
        return getClaimFromToken(token, Claims::getExpiration);
    }

    public <T> T getClaimFromToken(String token, Function<Claims, T> claimsResolver) {
        final Claims claims = getAllClaimsFromToken(token);
        return claimsResolver.apply(claims);
    }
    //for retrieveing any information from token we will need the secret key
    private Claims getAllClaimsFromToken(String token) {
        return Jwts.parser().setSigningKey(secret).parseClaimsJws(token).getBody();
    }

    //check if the token has expired
    private Boolean isTokenExpired(String token) {
        final Date expiration = getExpirationDateFromToken(token);
        return expiration.before(new Date());
    }

    //generate token for user
    public String generateToken(UserDetails userDetails) {
        Map<String, Object> claims = new HashMap<>();
        claims.put("nombre", "rosa");
        claims.put("role",userDetails.getAuthorities().stream().map(r->r.getAuthority()).collect(Collectors.joining()));
        return doGenerateToken(claims, userDetails.getUsername());
    }

    //while creating the token -
    //1. Define  claims of the token, like Issuer, Expiration, Subject, and the ID
    //2. Sign the JWT using the HS512 algorithm and secret key.
    //3. According to JWS Compact Serialization(https://tools.ietf.org/html/draft-ietf-jose-json-web-signature-41#section-3.1)
    //   compaction of the JWT to a URL-safe string
    private String doGenerateToken(Map<String, Object> claims, String subject) {

        return Jwts.builder().setClaims(claims).setSubject(subject).setIssuedAt(new Date(System.currentTimeMillis()))
                .setExpiration(new Date(System.currentTimeMillis() + JWT_TOKEN_VALIDITY))
                .signWith(SignatureAlgorithm.HS512, secret).compact();
    }

    //validate token
    public Boolean validateToken(String token, UserDetails userDetails) {
        final String username = getUsernameFromToken(token);
        return (username.equals(userDetails.getUsername()) && !isTokenExpired(token));
    }
}
```

### WebSecurityConfig

```java
@Configuration
@EnableWebSecurity
@EnableGlobalMethodSecurity(prePostEnabled = true)
public class WebSecurityConfig {

    @Autowired
    private JwtAuthenticationEntryPoint jwtAuthenticationEntryPoint;

    @Autowired
    private UserDetailsService jwtUserDetailsService;

    @Autowired
    private JwtRequestFilter jwtRequestFilter;

    @Autowired
    @Qualifier("handlerExceptionResolver")
    private HandlerExceptionResolver exceptionResolver;

    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration authenticationConfiguration) throws Exception {
        return authenticationConfiguration.getAuthenticationManager();
    }

    @Bean
    public static PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Autowired
    public void configureGlobal(AuthenticationManagerBuilder auth) throws Exception {
        auth.userDetailsService(jwtUserDetailsService).passwordEncoder(passwordEncoder());
    }

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity httpSecurity) throws Exception {
        httpSecurity
                .csrf().disable()
                .authorizeRequests()
                .antMatchers("/authenticate").permitAll() //.hasAuthority("ADMIN")
                .anyRequest().authenticated()
                .and()
                .exceptionHandling().authenticationEntryPoint(jwtAuthenticationEntryPoint)
                .and()
                .formLogin().disable()
                .sessionManagement()
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS);

        httpSecurity.addFilterBefore(jwtRequestFilter, UsernamePasswordAuthenticationFilter.class);

        return httpSecurity.build();
    }
}
```

### Entities

### Role.java

Código:
```java
@Entity
@Table(name = "roles", uniqueConstraints = { @UniqueConstraint(columnNames = { "user_id", "rol" }) })
public class Role implements Serializable {

	private static final long serialVersionUID = 1L;

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;

	private String rol;
	
	@ManyToOne
	@JoinColumn(name="user_id", nullable=false)
	private Users user;
	
	// Generate > Getter and setter (Select all)
}
```

### Users.java

Código:
```java
@Entity
@Table(name = "users")
public class Users implements Serializable {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;

	@Column(length = 30, unique = true)
	private String username;
	@Column(length = 200)
	private String password;
	private Boolean enabled;
	@OneToMany(fetch = FetchType.EAGER, cascade = CascadeType.ALL)
	@JoinColumn(name = "user_id")
	private List<Role> roles;

	// Generate > Getter and setter (Select all)
}
```
### Repository

### UserRepository.java (Tipo interfaz)

Código:
```java
@Repository
public interface UserRepository extends JpaRepository<Users, Long> {
	public Users findByUsername(String username);
	
	@Query("select count(u.username) from Users u where u.username =:username")
	public int buscarUsername(@Param("username") String nombre);
	
	@Transactional
	@Modifying
	@Query(value = "insert into roles (rol, user_id) VALUES (:rol, :user_id)", nativeQuery = true)
	public void insRol(@Param("rol") String authority, @Param("user_id") Long user_id);
}
```

### RoleRepository.java (Tipo interfaz)

Código:
```
@Repository
public interface RoleRepository extends JpaRepository<Role, Long> {

}
```

### Service Implements

### JwtUserDetailsService.java

Código
```java
@Service
public class JwtUserDetailsService implements UserDetailsService {
    @Autowired
    private UserRepository repo;

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        Users user = repo.findByUsername(username);

        if(user == null) {
            throw new UsernameNotFoundException(String.format("User not exists", username));
        }

        List<GrantedAuthority> roles = new ArrayList<>();

        user.getRoles().forEach(rol -> {
            roles.add(new SimpleGrantedAuthority(rol.getRol()));
        });

        UserDetails ud = new org.springframework.security.core.userdetails.User(user.getUsername(), user.getPassword(), user.getEnabled(), true, true, true, roles);

        return ud;
    }
}
```

### Controllers

### JwtAuthenticationController.java

Código:
```java
@RestController
@CrossOrigin
public class JwtAuthenticationController {
	@Autowired
	private AuthenticationManager authenticationManager;
	@Autowired
	private JwtTokenUtil jwtTokenUtil;
	@Autowired
	private JwtUserDetailsService userDetailsService;
	@PostMapping("/authenticate")
	public ResponseEntity<?> createAuthenticationToken(@RequestBody JwtRequest authenticationRequest) throws Exception {
		authenticate(authenticationRequest.getUsername(), authenticationRequest.getPassword());
		final UserDetails userDetails = userDetailsService.loadUserByUsername(authenticationRequest.getUsername());
		final String token = jwtTokenUtil.generateToken(userDetails);
		return ResponseEntity.ok(new JwtResponse(token));
	}
	private void authenticate(String username, String password) throws Exception {
		try {
			authenticationManager.authenticate(new UsernamePasswordAuthenticationToken(username, password));
		} catch (DisabledException e) {
			throw new Exception("USER_DISABLED", e);
		} catch (BadCredentialsException e) {
			throw new Exception("INVALID_CREDENTIALS", e);
		}
	}
}
```

## Dar autorizaciones
El código a continuación se utiliza en los controlers de la entidad con el método que se le quiera dar autorización. Se debe usar antes del @Get..., @Post..., @Delete.., @Put... Mapping. Acá el código:
```java
@PreAuthorize("hasAuthority('ADMIN')")
```
## Testing
###### Añadir usuario de test
El primer usuario tipo ADMIN se añade directamente desde PgAdmin. Sus credenciales son:
- Username: `admin`
- Password: `$2a$12$Y21e0xS32N4nQvpsV52M/Obn8KWx4fRSxkT2ERhMjA.kNVkEtYZjW` (admin)
###### Postman login query
- Mapeo: **POST**
- Body: Json
- Body content:  
```json
{
    "username":"admin",
    "password":"admin"
}
```
###### Probar autenticación
Requiere poner en el header del request:
- Key: `Authorization`
- Value: `Bearer [token]` (sin \[\])