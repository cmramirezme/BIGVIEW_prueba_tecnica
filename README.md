# ✈️ API Gateway para Microservicios de Gestión y Reservas de Vuelos

## 📌 Descripción del Proyecto

Este proyecto implementa un **API Gateway** que centraliza la comunicación entre múltiples microservicios desarrollados en Python. Sus principales funciones son:

- 🔐 **Gestión de Usuarios**: Registro, autenticación y validación de usuarios.
- ✈️ **Gestión de Vuelos**: Búsqueda, reserva, consulta y cancelación de vuelos.

El API Gateway actúa como punto único de entrada, gestionando la autenticación mediante **tokens JWT** y redirigiendo las solicitudes al microservicio correspondiente.

---

## ⚙️ Instalación y Ejecución

### Requisitos Previos

- [Docker](https://www.docker.com/) y Docker Compose
- [Postman](https://www.postman.com/): Para probar los endpoints

### Pasos para la Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/cmramirezme/BIGVIEW_prueba_tecnica.git
   cd BIGVIEW_prueba_tecnica
   git checkout master
   ```

2. Ejecutar los contenedores:
   ```bash
   docker-compose up -d
   ```

---

## 🚀 Uso de la Aplicación

### Pruebas con Postman

1. Abrir Postman.
2. Importar la colección `Pruebas Flights.postman_collection.json` ubicada en la raíz del repositorio.
3. Usar las solicitudes preconfiguradas para interactuar con el sistema.

---

## 📬 Endpoints Disponibles

### 🔸 1. Registro de Usuario

- **Método**: `POST`
- **Ruta**: `/register`
- **Body (JSON)**:
  ```json
  {
    "username": "Usuario",
    "password": "hola1234"
  }
  ```
- **Respuesta Exitosa**:
  ```json
  {
    "message": "Usuario registrado exitosamente."
  }
  ```

---

### 🔸 2. Inicio de Sesión

- **Método**: `GET`
- **Ruta**: `/login`
- **Body (JSON)**:
  ```json
  {
    "username": "user1",
    "password": "contraseña1"
  }
  ```
- **Respuesta Exitosa**:
  ```json
  {
    "message": "Inicio de sesión exitoso.",
    "token": "<JWT_TOKEN>"
  }
  ```

---

### 🔸 3. Buscar Vuelos

- **Método**: `GET`
- **Ruta**: `/flights/search`
- **Header**:
  - `Authorization: Bearer <JWT_TOKEN>`
- **Body (JSON)**:
  ```json
  {
    "origin": "San Andrés",
    "destination": "Santa Marta",
    "date": "2025-04-09T00:00:00.000+00:00"
  }
  ```
- **Respuesta Exitosa**:
  ```json
  {
    "_id": { "$oid": "..." },
    "origen": "San Andrés",
    "destino": "Santa Marta",
    "fecha": { "$date": "2025-04-09T00:00:00Z" },
    "user": null
  }
  ```

---

### 🔸 4. Reservar Vuelos

- **Método**: `POST`
- **Ruta**: `/flights/book`
- **Header**:
  - `Authorization: Bearer <JWT_TOKEN>`
- **Body (JSON)**:
  ```json
  {
    "toBooking": ["67fa73cc890eab8cbef16641"]
  }
  ```
- **Respuesta Exitosa**:
  ```json
  {
    "matched_count": 1,
    "modified_count": 1,
    "user_id": "67f92986b423330fa6f1775d",
    "message": "Vuelos reservados."
  }
  ```

---

### 🔸 5. Consultar Mis Reservas

- **Método**: `POST`
- **Ruta**: `/flights/my-reservations`
- **Header**:
  - `Authorization: Bearer <JWT_TOKEN>`
- **Body**: vacío
- **Respuesta Exitosa**:
  ```json
  {
    "_id": { "$oid": "..." },
    "origen": "San Andrés",
    "destino": "Santa Marta",
    "fecha": { "$date": "2025-04-09T00:00:00Z" },
    "user": { "$oid": "67f92986b423330fa6f1775d" }
  }
  ```

---

### 🔸 6. Cancelar Vuelos

- **Método**: `POST`
- **Ruta**: `/flights/cancel`
- **Header**:
  - `Authorization: Bearer <JWT_TOKEN>`
- **Body (JSON)**:
  ```json
  {
    "toCancel": ["67fa73cc890eab8cbef16641"]
  }
  ```
- **Respuesta Exitosa**:
  ```json
  {
    "matched_count": 1,
    "modified_count": 1,
    "user_id": "67f92986b423330fa6f1775d",
    "message": "Vuelos cancelados."
  }
  ```

---

## 🧑‍💻 Autor

Proyecto desarrollado por [cmramirezme](https://github.com/cmramirezme) como prueba técnica para BIGVIEW.

---
