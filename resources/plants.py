import models

from flask import Blueprint, jsonify, request

from flask_login import current_user, login_required

from playhouse.shortcuts import model_to_dict



plant = Blueprint('plants', 'plant')

@plant.route('/', methods=['GET'])
@login_required
def plant_index():
	try:
		#find all plants that have an owner matching the logged in users id
		print('tis is the currnet user.id in plant_index')
		print(current_user.id)
		this_users_plant_instances = models.Plant.select().where(
			models.Plant.owner_id == current_user.id
		)
		this_users_plant_dicts = [model_to_dict(plant) for plant in this_users_plant_instances]

		return jsonify(data=this_users_plant_dicts, status={
			'code': 200,
			'message': 'Sucess'
			}), 200

	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message': 'Error getting the resources'}), 401
		

#define route to create a plant
@plant.route('/', methods=['POST'])
@login_required
def create_plant():
		#this will get contain the info to create the plant
		payload = request.get_json()
		#**payload is the spread operator containing the new plants info
		plant = models.Plant.create(
				name=payload['name'],
				alias=payload['alias'],
				origin=payload['origin'],
				owner=current_user.id
		)
		#turn the plant model into a dictionary
		print(model_to_dict(plant), 'model to dict') 
		plant_dict = model_to_dict(plant)
		#return the jsonified object and a status code indicating sucess or error with password removed
		plant_dict['owner'].pop('password')
		return jsonify(data=plant_dict, status={'code': 201, 'message': 'success'}), 201

#show a single plant by id
@plant.route('<id>', methods=['GET'])
#retrieve plant by id that is being passed down 
def get_one_plant(id):
	#if successful display found plants informtion
	plant = models.Plant.get_by_id(id)
	if not current_user.is_authenticated:
		return jsonify(data={
				'name': plant.name,
				'alias': plant.alias,
				'origin': plant.origin
			}, status={
				'code': 200,
				'message': 'Registered users can access more info about this plant'
			}), 200
			#if unsuccessful return error message and no info
	else:
		plant_dict = model_to_dict(plant)
		#remove pw from return object
		plant_dict['owner'].pop('password')
		#must b logged in to see when plant was created
		if plant.owner_id != current_user.id:
			plant_dict.pop('created at')

		return jsonify(data=plant_dict, status={
				'code': 200,
				'message': 'Found plant with id {}'.format(plant.id)
			}), 200

#define route to update a plant by passing it's id through to the function
@plant.route('/<id>', methods=['PUT'])
@login_required
def update_plant(id):
		payload = request.get_json()

		plant = models.Plant.get_by_id(id)

		#check to see if dog belongs to user that ais logged in
		if(plant.owner.id == current_user.id):
			#else None must be included to avoid error
			plant.name = payload['name'] if 'name' in payload else None
			plant.alias = payload['alias'] if 'alias' in payload else None
			plant.origin = payload['origin'] if 'origin' in payload else None
			#save updates
			plant.save()

			plant_dict = model_to_dict(plant)
			plant_dict['owner'].pop('password')

			return jsonify(data=plant_dict, status={
					'code': 200,
					'message': 'Resource updated successfully'
				}), 200

		else:
			return jsonify(data='Forbidden', status={
				'code': 403,
				'message': 'A user can only update their own plants'
				}), 403

		return jsonify(data=model_to_dict(plant), status={'code': 200, 'message': 'Resource updated successfully'}), 200

#define route to delete plant by id
@plant.route('/<id>', methods=['DELETE'])
@login_required
def delete_plant(id):
	plant_to_delete = models.Plant.get_by_id(id)

	if plant_to_delete.owner.id != current_user.id:
		return jsonify(data='Forbidden', status={
			'code': 403,
			'message': 'A user can only update their own plants'
			}), 403
	else:
		plant_name = plant_to_delete.name
		plant_to_delete.delete_instance()
		return jsonify(data='Resource successfully deleted', status={
			'code': 200,
			'message': '{} deleted successfully'.format(plant_name)
			})

	









