from flask import Flask, render_template, request, redirect, url_for, jsonify, json

from flask_swagger_ui import get_swaggerui_blueprint
from flask import Blueprint

# notification_api_blueprint = Blueprint('notification_api', __name__)
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, GymPackageModel


SWAGGER_URL = '/api/docs'
API_URL = '/api/gympackage/docs.json'

swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
    )
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)




# Connect to Database and create database session
# engine = create_engine('sqlite:///advertise-service?check_same_thread=False')
# engine = create_engine('mysql+mysqlconnector://root:1234@localhost:3306/advertise_service')
engine = create_engine('mysql+mysqlconnector://root:1234@flexigym-advertise-service2-db/advertise-service')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


"""
api functions
"""
from flask import jsonify


def getPackages():
    packages = session.query(GymPackageModel).all()
    return jsonify(packages=[b.serialize for b in packages])


def getPackage(package_id):
    packages = session.query(GymPackageModel).filter_by(id=package_id).one()
    return jsonify(packages=packages.serialize)


def createNewGymPackage(package_name, package_description, price, available_qty):
    addedpackage = GymPackageModel(package_name=package_name, package_description=package_description, price=price, available_qty=available_qty)
    session.add(addedpackage)
    session.commit()
    return jsonify(package=addedpackage.serialize)


def updatePackage(id, package_name, package_description, price, available_qty):
    updatedPackage = session.query(GymPackageModel).filter_by(id=id).one()
    if not package_name:
        updatedPackage.package_name = package_name
    if not package_description:
        updatedPackage.package_description = package_description
    if not price:
        updatedPackage.genre = price
    if not available_qty:
        updatedPackage.available_qty = available_qty
    session.add(updatedPackage)
    session.commit()
    return 'Updated a Package with id %s' % id


def deletePackage(id):
    packageToDelete = session.query(GymPackageModel).filter_by(id=id).one()
    session.delete(packageToDelete)
    session.commit()
    return 'Removed Package with id %s' % id


@app.route('/')
@app.route('/packagesApi', methods=['GET', 'POST'])
def gymPackagesFunction():
    if request.method == 'GET':
        return getPackages()
    elif request.method == 'POST':
        package_name = request.args.get('package_name', '')
        package_description = request.args.get('package_description', '')
        price = request.args.get('price', '')
        available_qty = request.args.get('available_qty', '')
        return createNewGymPackage(package_name, package_description, price, available_qty)


@app.route('/packagesApi/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def gymPackagesFunctionId(id):
    if request.method == 'GET':
        return getPackage(id)

    elif request.method == 'PUT':
        package_name = request.args.get('package_name', '')
        package_description = request.args.get('package_description', '')
        price = request.args.get('price', '')
        available_qty = request.args.get('available_qty', '')
        return updatePackage(id, package_name, package_description, price, available_qty)

    elif request.method == 'DELETE':
        return deletePackage(id)


@app.route("/api/gympackage/docs.json", methods=['GET'])
def swagger_api_docs_yml():
    with open('swagger.json') as fd:
        json_data = json.load(fd)

    return jsonify(json_data);


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=4996)