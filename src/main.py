from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

#instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin@localhost:3306/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()

@app.route("/")
def root():
    return "Home"

db = SQLAlchemy(app)
ma = Marshmallow(app)

#create a model (table) only once
class Customer(db.Model):
    no = db.Column('No.',db.String(20), primary_key=True)  #first parameter in Column is the name of the column in the table
    name = db.Column('Name',db.String(100))

    def __init__(self,no,name):
        self.no = no        
        self.name = name        

db.create_all()

#Schema
class CustomerSchema(ma.Schema):
    class Meta:
        fields = ('no', 'name')

#one record
customer_schema = CustomerSchema()
#many records
customers_schema = CustomerSchema(many=True)

#GET
@app.route("/customers", methods=["GET"])
def getCustomers():
    customers = Customer.query.all()
    result = customers_schema.dump(customers)
    return jsonify(result)

#GET By ID
@app.route("/customers/<no>", methods=["GET"])
def getCustomer(no):
    customer = Customer.query.get(no)
    return customer_schema.jsonify(customer)

#POST
@app.route("/customers", methods=["POST"])
def addCustomer():
    no = request.json['no']
    name = request.json['name']

    new_customer = Customer(no, name)

    db.session.add(new_customer)
    db.session.commit()

    return customer_schema.jsonify(new_customer)

#PUT
@app.route("/customers/<no>", methods=["PUT"])
def updateCustomer(no):
    customer = Customer.query.get(no)

    no = request.json['no']
    name = request.json['name']

    customer.no = no
    customer.name = name

    db.session.commit()

    return customer_schema.jsonify(customer)

#DELETE
@app.route("/customers/<no>", methods=["DELETE"])
def deleteCustomer(no):
    customer = Customer.query.get(no)

    db.session.delete(customer)
    db.session.commit()

    return customer_schema.jsonify(customer)


# @app.route("/users/<int:id>")
# def getUser(id):
#     user={
#         "id":id,
#         "name":"John Doe",
#         "email":"john.doe@niccoweb.com"}
#     # /users/2654?query=query_test
#     query = request.args.get("query")
#     if query:
#         user["query"] = query
#     return jsonify(user),200

# @app.route("/users", methods=["POST"])
# def createUser():
#     data = request.get_json()
#     data["status"] = "created"
#     return jsonify(data),201

#run the app
if __name__ == '__main__':
    app.run(debug=True)

