from flask import Flask, render_template, request, redirect, url_for
import pymongo
from bson.objectid import ObjectId

app = Flask(__name__)
cliente = pymongo.MongoClient("mongodb://localhost:27017")
db = cliente['alumno']


@app.route("/")
def listado():
    alumnos = db['clase']
    resultado = alumnos.find()

    # el resultado que devuelve find() es una colección
    # y debo convertirlo a una lista de objetos para
    # pasarlo a la plantilla

    salida = []
    for x in resultado:
        print(x)
        salida.append(x)

    return render_template("listado.html", clase=salida)


@app.route("/api/nuevo", methods=['GET'])
def nuevo_alumno():
    return render_template("formulario.html")


@app.route("/api/nuevo", methods=['POST'])
def guardar_alumno():
    nombre = request.form['nombre']
    apellidos = request.form['apellidos']

    alumnos = db['clase']
    nuevo_al = {"nombre": nombre, "apellido": apellidos}
    alumnos.insert_one(nuevo_al)

    return redirect(url_for('listado'))


@app.route("/api/<string:id>", methods=['GET'])
def mostrar_alumno(id):
    alumnos = db['clase']
    info = alumnos.find_one({"_id": ObjectId(id)})
    # info = alumnos.find( { "nombre" : "Juan" } )
    # info = alumnos.find( { "$and" : [  { "$or" : [ { "nombre":"Juan" }, {"nombre":"Pepe"} ]  }  , {"apellidos":"Sotillo"} ]   } )

    print(str(info))
    return render_template("saludo.html", clase="verde", nombre=info['nombre'], apellido=info['apellido'])


@app.route("/api/<string:nombre>/<string:apellido>", methods=['GET'])
def hello_api(nombre, apellido):
    return render_template("saludo.html", clase="verde", nombre=nombre, apellido=apellido)


app.run()
