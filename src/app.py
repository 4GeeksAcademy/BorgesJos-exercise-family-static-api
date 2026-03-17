"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# GET: Mostrar Miembros de la familia
@app.route('/members', methods=['GET'])
def handle_hello():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    return jsonify(members), 200


# POST: Crear nuevo miembro
@app.route('/members', methods=['POST'])
def add_member():
    new_member = request.json
    jackson_family.add_member(new_member)

    return jsonify(new_member), 200


# GET: Obtener un miembro de la familia especifico
@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    find_member = jackson_family.get_member(id)
    if not find_member:
        return jsonify({"msg": "No se encontro al miembro"}), 400
    return jsonify(find_member), 200


# # PUT: Actualizar miembro de la familia
# @app.route('/member/<int:member_id>', methods=['PUT'])
# def actualizar_member(member_id):
#     new_member = request.json()
#     update_member = jackson_family.update_member(member_id, new_member)
#     if not update_member:
#         return jsonify({"msg": "No se encontro al miembro"}), 400
#     return jsonify({"DONE!!": "Familiar Actualizado"}), 200


# DELETE: Borrar miembro de la familia
@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    # This is how you can use the Family datastructure by calling its methods
    eliminar_f = jackson_family.delete_member(id)
    if not eliminar_f:
        return jsonify({"msg": "Familiar no encontrado"}), 400
    
    return jsonify({"done": True}), 200

# GET: Obtener un miembro de la familia especifico
# @app.route('/member/<int:member_id>', methods=['GET'])
# def get_member(member_id):
#     find_member = jackson_family.get_member(member_id)
#     if not find_member:
#         return jsonify({"msg": "No se encontro al miembro"}), 400
#     return jsonify(find_member), 200


# @app.route('/member/<int:member_id>', methods=['PUT'])
# def actualizar_member(member_id):
#     new_member = request.json()
#     update_member = jackson_family.update_member(member_id, new_member)
#     if not update_member:
#         return jsonify({"msg": "No se encontro al miembro"}), 400
#     return jsonify({"DONE!!": "Familiar Actualizado"}), 200


# @app.route('/member/<int:member_id>', methods=['GET'])
# def get_member(member_id):
#     find_member = jackson_family.get_member(member_id)
#     if not find_member:
#         return jsonify({"msg": "No se encontro al miembro"}), 400
#     return jsonify(find_member), 200




# @app.route('/nuevo', methods=['GET'])
# def add_member():
#     # This is how you can use the Family datastructure by calling its methods
#     members = jackson_family.get_all_members()
#     response_body = {"hello": "world",
#                      "family": members}
#     return jsonify(response_body), 200



# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
