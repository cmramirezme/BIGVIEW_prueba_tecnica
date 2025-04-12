from flask import Flask, request,jsonify, Response
from flask_pymongo import PyMongo
from bson import json_util
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
mongo = MongoClient("mongodb://flight-search-db:27017/")  # Cambia la URI si es diferente
db = mongo["FlightDB"]  # Nombre de la base de datos

@app.route('/search',methods=['Get'])
def give_flights():
    origin=request.json['origin']
    destination=request.json['destination']
    date = datetime.strptime(request.json['date'], "%Y-%m-%dT%H:%M:%S.%f%z")
    print(request.json)
    print('holaMundo')
    if origin and destination and date:
        #esta funcion obtiene los datos en formato Bson
        flights = db.Flights.find({
            'origen':{'$eq':origin},
            'destino':{'$eq':destination},
            'fecha' : {'$eq':date}
        })
        
        response=json_util.dumps(flights) # Aqui se pasa de Bson a Json
        return Response(response,mimetype='application/json')


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