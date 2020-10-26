from datetime import datetime
from flask import request, jsonify, make_response, url_for, redirect
from .models import GymPackageModel, db
from service import advertise_api_blueprint
from functools import wraps
import requests

USER_API_OK = True
USER_URL = "https://flexigym.rohitzariwal.co.in/auth"


@advertise_api_blueprint.route('/test')
def hello_world():
    return 'test!'


'''
input: auth token
output: flag, response
'''


def is_admin(auth_token):
    headers = {'Authorization': 'Bearer ' + auth_token,
               'Content-Type': 'application/json'
               }
    try:
        response = requests.get(url=USER_URL + "/status", headers=headers)
        if response.status_code == 200:
            return response.json()['data']['admin'], response
        else:
            return "error", response
    except Exception as e:
        print(e)
        responseObject = {
            'status': 'fail',
            'message': 'Authorization server request fail'
        }
        return "error", (make_response(jsonify(responseObject)), 500)


def login_required(f):
    @wraps(f)
    def check_jwt_header(*args, **kwargs):
        # check for every request method other than GET
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''

        if not auth_token:
            responseObject = {
                'status': 'fail',
                'message': 'Not authorised, Please login!'
            }
            return make_response(jsonify(responseObject)), 401
        else:
            # check token status here...
            admin_flag, response = is_admin(auth_token)

            # if the user is not an admin and request is not GET
            if not admin_flag and request.method != "GET":
                responseObject = {
                    'status': 'fail',
                    'message': 'Not authorised, You\'re not admin!'
                }
                return make_response(jsonify(responseObject)), 401

            # if the response from auth is not correct/ token expired
            elif admin_flag == "error":
                # if signature expired, forward the info to client
                return make_response(response.content), response.status_code

            # if the user is logged in as admin - OK
            else:
                pass

        return f(*args, **kwargs)

    return check_jwt_header


def getPackages():
    packages = GymPackageModel.query.all()
    response = make_response(jsonify(packages=[b.to_json for b in packages])), 200, {'Access-Control-Allow-Origin': '*'}
    return response


def getPackage(package_id):
    packages = GymPackageModel.query.filter_by(id=package_id).one()
    response = make_response(jsonify(packages=packages.to_json)), 200, {'Access-Control-Allow-Origin': '*'}
    return response


def createNewGymPackage(package_name, package_description, price, available_qty, valid_from, valid_to, created_by):
    try:
        valid_from = datetime.strptime(valid_from, '%Y-%m-%d  %H:%M:%S')
        valid_to = datetime.strptime(valid_to, '%Y-%m-%d  %H:%M:%S')
        addedpackage = GymPackageModel(package_name=package_name, package_description=package_description, price=price,
                                       available_qty=available_qty, valid_from=valid_from, valid_to=valid_to,
                                       created_by=created_by)
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

        updatedPackage.package_name = package_name
        updatedPackage.package_description = package_description
        updatedPackage.price = price
        updatedPackage.available_qty = available_qty
        updatedPackage.updated_by = updated_by

        # valid_from = datetime.strptime(valid_from, '%Y-%m-%d  %H:%M:%S')
        # valid_to = datetime.strptime(valid_to, '%Y-%m-%d  %H:%M:%S')
        # updatedPackage.valid_from = valid_from
        # updatedPackage.valid_to = valid_to
        updatedPackage.updated_date = datetime.now()

        print(updatedPackage.to_json)

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
        # return 'Removed Package with id %s' % id
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


@advertise_api_blueprint.route('/packagesApi/all', methods=['GET', 'POST'])
@login_required
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
        return createNewGymPackage(package_name, package_description, price, available_qty, valid_from, valid_to,
                                   created_by)


@advertise_api_blueprint.route('/packagesApi/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
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
        updated_by = request.args.get('updated_by', '')

        return updatePackage(id, package_name, package_description, price, available_qty, valid_from, valid_to,
                             updated_by)

    elif request.method == 'DELETE':
        return deletePackage(id)
