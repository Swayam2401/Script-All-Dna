from flask import Flask,request,jsonify
from controller.library import Library

library = Library()

app = Flask(__name__)

#signUp method
@app.post("/signup")
def signUp():
    data = None

    if(request.is_json):
        data = request.get_json()

    print(data)

    if(not data):
        return jsonify({"message" : "no data available"}),400
    
    userId = data.get("userId")
    name = data.get("name")
    isPremium = data.get("isPremium")

    if(library.addMember(name,userId,isPremium)):
        return jsonify(library.showBooks()),200
    
    return jsonify({"message" : "user id already available"}),404

#Login method
@app.get("/login/<userName>/<userId>")
def login(userName,userId):
    member = library.fetchMember(userId,userName)

    if(member):
        return jsonify(library.showBooks()),200
    
    return jsonify({"message" : "user id or name not matched"}),404

#borrowBook method
@app.patch("/borrowbook/<userId>/<bookName>/<qty>")
def borrowBook(userId,bookName,qty):
    return jsonify({"message" : library.borrowBook(int(userId),bookName,int(qty))})

#returnBook method
@app.patch("/returnbook/<userId>/<bookName>/<qty>")
def returnBook(userId,bookName,qty):
    return jsonify({"message" : library.returnBook(int(userId),bookName,int(qty))})

#member delete method
@app.delete("/removemember/<userId>/<userName>")
def removeMember(userId,userName):
    library.removeMember(userId,userName)

    return jsonify({"message" : "removed"}),204


#show borrowed Books
@app.get("/showborrowed/<userId>")
def showBorrowed(userId):
    return jsonify(library.getAllBorrowed(userId))

#show all members
@app.get("/showmembers")
def showMembers():
    return jsonify(library.showMembers())



if(__name__ == "__main__"):
    app.run(debug=True)



        








