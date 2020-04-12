from datetime import datetime
from flask import request, jsonify, make_response
from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker
from service.models import GymPackageModel, db
from . import advertise_api_blueprint


# service-endpoint
Session = sessionmaker(bind=engine)
session = Session()

@advertise_api_blueprint.route('/test')
def hello_world():
    return 'test!'


def getPackages():
    packages = GymPackageModel.query.all()
    return make_response(jsonify(packages=[b.to_json for b in packages])), 200

def getPackage(package_id):
    packages = GymPackageModel.query.filter_by(id=package_id).one()
    return make_response(jsonify(packages=packages.to_json)), 200

def createNewGymPackage(package_name, package_description, price, available_qty, valid_from, valid_to, created_by):
    try:
        valid_from = datetime.strptime(valid_from, '%Y-%m-%d  %H:%M:%S')
        valid_to = datetime.strptime(valid_to, '%Y-%m-%d  %H:%M:%S')
        addedpackage = GymPackageModel(package_name=package_name, package_description=package_description, price=price,
                                       available_qty=available_qty, valid_from=valid_from, valid_to=valid_to, created_by=created_by)
        addedpackage.created_date = datetime.now()
        addedpackage.updated_date = datetime.now()
        db.session.add(addedpackage)
        db.session.commit()

        # return package if success.
        responseObject = {
            'status': 'success',
            'package': addedpackage.to_json
        }
        return make_response(jsonify(responseObject)), 200
    except Exception as e:
        print(e)
        responseObject = {
            'status': 'fail',
            'message': 'Something went wrong!'
        }
        return make_response(jsonify(responseObject)), 500

def updatePackage(id, package_name, package_description, price, available_qty, valid_from, valid_to, updated_by):
    try:
        updatedPackage = GymPackageModel.query.filter_by(id=id).one()
        if not package_name:
            updatedPackage.package_name = package_name
        if not package_description:
            updatedPackage.package_description = package_description
        if not price:
            updatedPackage.genre = price
        if not available_qty:
            updatedPackage.available_qty = available_qty
        if not updated_by:
            updatedPackage.updated_by = updated_by

        updatedPackage.valid_from = valid_from
        updatedPackage.valid_to = valid_to
        updatedPackage.updated_date = datetime.now()
        db.session.add(updatedPackage)
        db.session.commit()
        # return 'Updated a Package with id %s' % id
        responseObject = {
            'status': 'success',
            'package': updatedPackage.to_json
        }
        return make_response(jsonify(responseObject)), 200
    except Exception as e:
        print(e)
        responseObject = {
            'status': 'fail',
            'message': 'Something went wrong!'
        }
        return make_response(jsonify(responseObject)), 500

def deletePackage(id):
    try:
        packageToDelete = GymPackageModel.query.filter_by(id=id).one()
        db.session.delete(packageToDelete)
        db.session.commit()
        #return 'Removed Package with id %s' % id
        responseObject = {
            'status': 'success',
            'package': packageToDelete.to_json
        }
        return make_response(jsonify(responseObject)), 200
    except Exception as e:
        print(e)
        responseObject = {
            'status': 'fail',
            'message': 'Something went wrong!'
        }
        return make_response(jsonify(responseObject)), 500

@advertise_api_blueprint.route('/')
@advertise_api_blueprint.route('/packagesApi', methods=['GET', 'POST'])
def gymPackagesFunction():
    if request.method == 'GET':
        return getPackages()

    elif request.method == 'POST':
        package_name = request.args.get('package_name', '')
        package_description = request.args.get('package_description', '')
        price = request.args.get('price', '')
        available_qty = request.args.get('available_qty', '')
        valid_from = request.args.get('valid_from', '')
        valid_to = request.args.get('valid_to', '')
        created_by = request.args.get('created_by', '')
        return createNewGymPackage(package_name, package_description, price, available_qty, valid_from, valid_to, created_by)

@advertise_api_blueprint.route('/packagesApi/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def gymPackagesFunctionId(id):
    if request.method == 'GET':
        return getPackage(id)

    elif request.method == 'PUT':
        package_name = request.args.get('package_name', '')
        package_description = request.args.get('package_description', '')
        price = request.args.get('price', '')
        available_qty = request.args.get('available_qty', '')
        valid_from = request.args.get('valid_from', '')
        valid_to = request.args.get('valid_to', '')
        return updatePackage(id, package_name, package_description, price, available_qty, valid_from, valid_to)

    elif request.method == 'DELETE':
        return deletePackage(id)
