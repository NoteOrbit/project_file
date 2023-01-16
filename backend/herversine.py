import math

class Haversine:

    def __init__(self,coord1,coord2):
        lon1,lat1=coord1
        lon2,lat2=coord2
        
        R=6371000                               # radius of Earth in meters
        phi_1=math.radians(lat1)
        phi_2=math.radians(lat2)

        delta_phi=math.radians(lat2-lat1)
        delta_lambda=math.radians(lon2-lon1)

        a=math.sin(delta_phi/2.0)**2+\
           math.cos(phi_1)*math.cos(phi_2)*\
           math.sin(delta_lambda/2.0)**2
        c=2*math.atan2(math.sqrt(a),math.sqrt(1-a))
        
        self.meters=R*c                         # output distance in meters
        self.km=self.meters/1000.0              # output distance in kilometers
        self.miles=self.meters*0.000621371      # output distance in miles
        self.feet=self.miles*5280


# @app.route('/nearby1',methods=["GET"])
# def recom_by():
#     latitude = request.args.get("latitude")
#     longitude = request.args.get("longitude")
#     db = client['Infomations']
#     collection = db['Store']
#     collection.create_index([("location", GEO2D)])
#     values = collection.find({},{'_id':1,'latitude':1,'longitude':1})

#     results = collection.find(
#         {
#             "location": {
#                 "$near": [float(longitude), float(latitude)],
#                 "$maxDistance": 1
#             }
#         }
#     )


#     return jsonify(list(results))



# @app.route("/nearby2", methods=["GET"])
# def nearby():
#     latitude = request.args.get("latitude")
#     longitude = request.args.get("longitude")
#     db = client['Infomations']
#     collection = db['Store']

#     if not all([latitude, longitude]):
#         return jsonify({"error": "Missing query parameters 'latitude' and 'longitude'"}), 400
#     try:
#         lat = float(latitude)
#         lon = float(longitude)
#     except ValueError:
#         return jsonify({"error": "Invalid value for 'latitude' and 'longitude'"}), 400

#     # Find documents with coordinates that are within 1km of the provided latitude and longitude
#     results = collection.find(
#         {
#             "latitude": { "$gte": lat - 0.01, "$lte": lat + 0.01},
#             "longitude": { "$gte": lon - 0.01, "$lte": lon + 0.01},
#         }
#     )
#     results = [x for x in results]
#     for i in range(len(results)):
#         results[i]['_id'] = str(results[i]['_id'])
#     return jsonify(results)

    
#     # for data in values:
#     #     output.extend(data)
#     # return {"data": output}


# #     # setup = Haversine()
# #     return Response(
# #     json_util.dumps(values),
# #     mimetype='application/json'
# # )
