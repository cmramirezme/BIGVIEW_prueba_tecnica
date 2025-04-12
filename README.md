# API Gateway para Microservicios de Gestión y Reservas de Vuelos

## Descripción del Proyecto
Este proyecto implementa un **API Gateway** que conecta múltiples microservicios desarrollados en Python. Los microservicios incluyen:
- **Gestión de usuarios**: Proporciona servicios de autenticación y manejo de usuarios.
- **Gestión de vuelos**: Permite realizar búsquedas, reservas y cancelaciones de vuelos.

El API Gateway actúa como punto único de entrada, gestionando la autenticación mediante tokens JWT y redirigiendo las solicitudes a los microservicios adecuados.

---

## Instrucciones para la Instalación y Ejecución

### **Requisitos previos**
1. **Docker y Docker Compose** : Para ejecutar los servicios en contenedores.
2. **Postman**: Para ejecutar las pruebas y hacer uso de la aplicacion

### **Instalación**
1. Clona este repositorio:
   ```bash
   git clone https://github.com/cmramirezme/BIGVIEW_prueba_tecnica.git
   cd BIGVIEW_prueba_tecnica
   
2. Poner en marcha los contenedores:
   Ejecuta la siguiente linea de codigo en bash dentro del repositorio clonado: docker-compose up -d
   Esto dejara lista la aplicacion para ser usada.

### **Uso**
1. Abrir el aplicativo Postman e importar el archivo "Pruebas Flights.postman_collection.json" ubicado en "BIGVIEW_prueba_tecnica" a un workspace. Alli
  se suministraran las solicitudes http ya estructuradas para probar el aplicativo

  - **Funcionalidad register**: No necesita token de autenticacion. Registra en la base de datos del microservicio "user-management" un nuevo usuario
    en caso de ya existir niega dicho registro.

    1. Metodo: POST
    2. body(JSON):
      {
        "username":"Usuario",
        "password":"hola1234"
   
      }
    3. Respuesta exitosa:
      {
        "message": "Usuario registrado exitosamente."
      }
  - **Funcionalidad login**: Envia usuario y contraseña para ser validados. En caso de exito suministra un token de autenticacion que debera ser copiado
    para enviarse en el header de otras solicitudes, de lo contrario negara el acceso y el token.

    1. Metodo: GET
    2. body(JSON):
      {
        "username":"user1",
        "password":"contraseña1"
   
      }
    3. Respuesta exitosa:
      {
        "message": "Inicio de sesión exitoso.",
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZXhwIjoxNzQ0NTE3NzAwfQ.9y2M3PNUllHsYDEotGSRhDNE_eq7g5l9xTLEgiEcoZk"
      }
    
  - **Funcionalidad Buscar Vuelos**: Necesita token de autenticacion suministrado al hacer uso de la funcionalidad "login". Lista los vuelos disponibles
    y se debe suministrar un body con el origen, el destino y la fecha del vuelo.

    1. Metodo: GET
    2. Header:
       * Authorization: Bearer <tu_token_jwt>
    3. body(JSON):
        {
          "origin":"San Andrés",
          "destination":"Santa Marta",
          "date": "2025-04-09T00:00:00.000+00:00"
        }
    4. Respuesta exitosa:
            
        {
            "_id": {
                "$oid": "67fa73cc890eab8cbef16641"
            },
            "destino": "Santa Marta",
            "fecha": {
                "$date": "2025-04-09T00:00:00Z"
            },
            "origen": "San Andrés",
            "user": null
        }
       
    

  - **Funcionalidad Reservar vuelos**: Necesita token de autenticacion suministrado al hacer uso de la funcionalidad "login". Envia un body con el conjunto
     id de vuelos que se quieren reservar (los cuales se pueden obtener de la respuesta al ejecutar "Buscar vuelos") y modifica la base de datos del 
    microservicio de vuelos, asignandoles a los vuelos el usuario con la sesion actual.

    1. Metodo: POST
    2. Header:
       * Authorization: Bearer <tu_token_jwt>
    3. body(JSON):
        {
          "toBooking":["67fa73cc890eab8cbef16641"]
        }
    4. Respuesta exitosa:
            
       {
        "matched_count": 1,
        "message": "Vuelos reservados.",
        "modified_count": 1,
        "user_id": "67f92986b423330fa6f1775d"
        }

  - **Funcionalidad Mis reservas**: Necesita token de autenticacion suministrado al hacer uso de la funcionalidad "login". Lista los vuelos reservados
    por el usuario en la sesion actual y no suministra un bofy en la solicitud.

    1. Metodo: POST
    2. Header:
       * Authorization: Bearer <tu_token_jwt>
    3. body(JSON):
        {
        }
    4. Respuesta exitosa:
            
       {
          "_id": {
              "$oid": "67fa73cc890eab8cbef16641"
          },
          "destino": "Santa Marta",
          "fecha": {
              "$date": "2025-04-09T00:00:00Z"
          },
          "origen": "San Andrés",
          "user": {
              "$oid": "67f92986b423330fa6f1775d"
          }
        }

   - **Funcionalidad Cancelar vuelos**: Necesita token de autenticacion suministrado al hacer uso de la funcionalidad "login". Envia un body con el conjunto
     id de vuelos que se quieren cancelar (los cuales se pueden obtener de la respuesta al ejecutar "Mis reservas") y modifica la base de datos del 
    microservicio de vuelos, desasignando a los vuelos suministrados el usuario con la sesion actual.

      1. Metodo: POST
      2. Header:
         * Authorization: Bearer <tu_token_jwt>
      3. body(JSON):
          {
            "toCancel":["67fa73cc890eab8cbef16641"]
          }
      4. Respuesta exitosa:
              
         {
            "matched_count": 1,
            "message": "Vuelos cancelados.",
            "modified_count": 1,
            "user_id": "67f92986b423330fa6f1775d"
          }
    
  
