from flask import Flask, request,jsonify, Response
from flask_pymongo import PyMongo
from bson import json_util
from pymongo import MongoClient
from datetime import datetime
import requests

app = Flask(__name__)
mongo = MongoClient("mongodb://flight-search-db:27017/")  
db = mongo["FlightDB"]  # Nombre de la base de datos

MICROSERVICES = {
    "api-gateway": "http://api-gateway:5000",  # Dirección del microservicio de Api gateway
}


@app.route('/search',methods=['GET'])
def give_flights():
    origin=request.json['origin']
    destination=request.json['destination']
    date = datetime.strptime(request.json['date'], "%Y-%m-%dT%H:%M:%S.%f%z")
    if origin and destination and date:
        #esta funcion obtiene los datos en formato Bson
        flights = db.Flights.find({
            'origen':{'$eq':origin},
            'destino':{'$eq':destination},
            'fecha' : {'$eq':date},
            'user' : {'$eq':None}
        })
        
        response=json_util.dumps(flights) # Aqui se pasa de Bson a Json
        return Response(response,mimetype='application/json')
    
@app.route('/booking',methods=['POST'])
def booking():
    try:
        # Obtener el JSON de la solicitud
        data = request.get_json()
        to_booking_ids = data.get("toBooking", [])

        if not to_booking_ids:
            return jsonify({"message": "No se proporcionaron IDs para reservar."}), 400
  
        # Obtener el token de la cabecera de la solicitud
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Token de autenticación no proporcionado."}), 401
        # Solicitar el ID del usuario al API Gateway
        user_id = get_user_id_from_api_gateway(token)
        if not user_id:
            return jsonify({"message":  "No se pudo obtener el id del usuario deseado" }), 401

        # Actualizar los documentos en la colección Flights
        result = db.Flights.update_many(
            {"_id": {"$in": to_booking_ids}},  # Coincidir con los IDs proporcionados
            {"$set": {"user": user_id}}       # Asignar el ID del usuario
        )

        return jsonify({
            "message": "Vuelos reservados.",
            "matched_count": result.matched_count,
            "modified_count": result.modified_count
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_user_id_from_api_gateway(token):
    """Obtiene el ID del usuario actual enviando una solicitud al API Gateway."""
    try:
        response = requests.get(f"{MICROSERVICES['api-gateway']}/user-management/id-user", headers={"Authorization": token})
        if response.status_code == 200:
            user_data = response.json()
            return user_data.get("user_id")  # Retorna el ID del usuario
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error al solicitar el ID de usuario: {str(e)}")
        return None
    

@app.errorhandler(404) #Manejo de errores
def not_found(error=None):
    response=jsonify({
        'message':'Resource Not Found:'+ request.url,
        'status':404
    })
    response.status_code=404
    return response
    
@app.route('/healthcheck', methods=['GET'])
def health_check():
    try:
        # Intentar listar las bases de datos para verificar la conexión
        db_list = mongo.list_database_names()
        return Response(json_util.dumps({"status": "success", "databases": db_list}),
                        status=200, mimetype='application/json')
    except Exception as e:
        # Manejar errores si no hay conexión
        return Response(json_util.dumps({"status": "error", "message": str(e)}),
                        status=500, mimetype='application/json')




if __name__== "__main__":
    app.run(host="0.0.0.0",port=5001,debug=True)