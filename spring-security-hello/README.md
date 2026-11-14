# Spring Boot 3.2 authenticated Hello World

Endpoints:

- `POST /api/login` with JSON `{"username":"test","password":"123456"}` creates an authenticated HTTP session.
- `GET /api/hello` requires that session and returns `Hello World`.
- `POST /api/logout` invalidates the session.

## Run

Requires Java 17+ and Maven 3.9+.

```bash
mvn test
mvn spring-boot:run
```

Example:

```bash
curl -i -c cookies.txt -H "Content-Type: application/json" \
  -d '{"username":"test","password":"123456"}' http://localhost:8080/api/login
curl -b cookies.txt http://localhost:8080/api/hello
```

The test credentials are intentionally in-memory demo credentials. Production deployments should load secrets from a secure identity system.
