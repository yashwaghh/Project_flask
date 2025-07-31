import os 
from flask import Flask, request , jsonify 
from bson.objectid import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


client = MongoClient(os.getenv("MONGO_URI"))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app=Flask(__name__)

db=client["library"]
items=db["books"]

@app.route("/books",methods=["POST"])
def create():
    data=request.get_json()

    result=items.insert_one(data)
    return jsonify({"message":str("Book added succesfully "),"_id":str(result.inserted_id)}),201

@app.route("/books",methods=["GET"])
def getall():
    docs=list()
    for doc in items.find():
        doc["_id"]=str(doc["_id"])
        docs.append(doc)
    return jsonify(docs),200

@app.route("/books/<id>",methods=["GET"])
def getspecific(id):
    doc=items.find_one({"_id":ObjectId(id)})
    doc["_id"]=str(doc["_id"])
    return jsonify(doc),200

@app.route("/books/<id>",methods=["PUT"])
def updatebook(id):
    data = request.get_json()

    result=items.update_one({"_id":ObjectId(id)},{"$set":data})
    return jsonify({"message":"Book updated successfully ","updated":result.modified_count}),200

@app.route("/books/<id>",methods=["DELETE"])
def deletebook(id):
    result=items.delete_one({"_id":ObjectId(id)})
    return jsonify({"message":str("Book deleted successfully")})

from flask import render_template

@app.route('/')
def index():
    docs = list()
    for doc in items.find():
        doc["_id"] = str(doc["_id"])
        docs.append(doc)
    return render_template("index.html", books=docs)



if __name__ =="__main__":
    app.run(debug=True)