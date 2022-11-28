from flask import Flask, Response, request
app = Flask(__name__)
import pymongo
from bson.objectid import ObjectId
import json
import os

MONGO_HOST = os.environ.get("MONGO_HOST")
MONGO_PORT = os.environ.get("MONGO_PORT")

try:
    mongo = pymongo.MongoClient(
        host= MONGO_HOST,
        port=MONGO_PORT,
        serverSelectionTimeoutMS=1000
    )
    mongo.server_info() # trigger exception if it cannot connect to database
    db = mongo.company
    print("connected successfully to db")
except:
    print("ERROR cannot connect to db")


@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    try:
        dbResponse = db.users.delete_one({"_id": ObjectId(id)}
        )
        if dbResponse.deleted_count == 1:
            return Response(
                response = json.dumps({"message": "user deleted", "id": f"{id}"}),
                status=200,
                mimetype="application/json"
            )
        return Response(
                response = json.dumps({"message": "user not found", "id": f"{id}"}),
                status=200,
                mimetype="application/json"
            )
    except Exception as ex:
        print("**************")
        print(ex)
        print("*****************")
        return Response(
            response = json.dumps({"message": "sorry cannot delete user"}),
            status=500,
            mimetype="application/json"
        )

@app.route("/users/<id>", methods=["PATCH"])
def update_user(id):
    try:
        dbResponse = db.users.update_one(
            {"_id": ObjectId(id)}, 
            {"$set": {"name": request.form["name"]}}
        )
       # for attr in dir(dbResponse):
        #    print(f"*******{attr}********")
        if dbResponse.modified_count == 1:
            return Response(
                response = json.dumps({"message": "user updated"}),
                status=200,
                mimetype="application/json"
            )
        return Response(
            response = json.dumps({"message": "nothing to update"}),
            status=200,
            mimetype="application/json"
        )

    except Exception as ex:
        print("******************")
        print(ex)
        print("******************")
        return Response(
            response = json.dumps({"message": "cannot update user"}),
            status=500,
            mimetype="application/json"
        )



@app.route("/users",methods=['POST'])
def create_user():
    try:
        user = {"name": request.form["name"], 
        "last_name": request.form["last_name"]}
        dbResponse = db.users.insert_one(user)
        print(dbResponse.inserted_id)
       # for attr in dir(dbResponse):
        #    print (attr)
        return Response(
            response = json.dumps({"message": "user created",
             "id": f"{dbResponse.inserted_id}"}),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print("*****************") 
        print(ex)
        print("*****************") 

@app.route("/users", methods=["GET"])
def get_some_users():
    try:
        data = list(db.users.find())
        for user in data:
            user["_id"] = str(user["_id"])
        return data
    except Exception as ex:
        print(ex)
        return Response(
            response = json.dumps({"message": "cannot read users"}),
            status=500,
            mimetype="application/json"
        )
############################
if __name__ == '__main__':
    app.run(port=8000, debug=True)



