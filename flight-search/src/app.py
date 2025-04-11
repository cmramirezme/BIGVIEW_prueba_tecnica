from flask import Flask, request,jsonify, Response
from flask_pymongo import PyMongo
from bson import json_util


app=Flask(__name__) #Crea una instancia de una aplicacion
app.config['MONGO_URI']='mongodb://flight-search-db:27017/FlightDB'

mongo=PyMongo(app) #Se obtiene coneccion a base de datos
"""
@app.route('/flight/country',methods=['POST'])#Creacion de rutas para añadir country (esta a la escuha)
def create_country():
    #Receiving country
    country_name=request.json['country_name'] #Los datos del Json recibido se almacena en variables
    if country_name:
        id=mongo.db.Country.insert_one(
            {'country_name':country_name}
        )
        response={
            'message':str(id),
            'country_name':country_name        
        }
        return response
    else:
        return not_found()
"""
@app.route('/search',methods=['Get'])
def give_flights():
    origin=request.json['origin']
    destination=request.json['destination']
    date=request.json['date']
    print(request.json)
    if origin and destination:
        #esta funcion obtiene los datos en formato Bson
        flights=mongo.db.Flight.find({'$and':[{'airport_origin.airport_origin_name':{'$eq':origin}},{'airport_destination.airport_destino_name':{'$eq':destination}}]})
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
    


if __name__== "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)