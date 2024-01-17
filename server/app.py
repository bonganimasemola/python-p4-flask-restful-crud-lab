from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Index(Resource):
    def get(self):
        response_dict = {
            "index": "Welcome to the [Compulsory]REST CRUD Lab",
        }

        response = make_response(jsonify(response_dict), 200)

        return response

api.add_resource(Index, '/')

class Plants(Resource):
    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        new_plant = Plant(
            name=request.form['name'],
            image=request.form['image'],
            price=request.form['price'],
        )

        db.session.add(new_plant)
        db.session.commit()

        response_dict = new_plant.to_dict()  

        response = make_response(jsonify(response_dict), 201)

        return response

api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(plant), 200)

    def patch(self, id):
        plant = Plant.query.get_or_404(id)

       
        if 'name' in request.form:
            plant.name = request.form['name']
        if 'image' in request.form:
            plant.image = request.form['image']
        if 'price' in request.form:
            plant.price = request.form['price']

        db.session.commit()

        response_dict = plant.to_dict()
        response = make_response(jsonify(response_dict), 200)

        return response

    def delete(self, id):
        plant = Plant.query.filter_by(id=id).first()

        if not plant:
            return make_response(jsonify({'error': 'Plant not found'}), 404)

        db.session.delete(plant)
        db.session.commit()

        return make_response({'message': 'Plant deleted successfully'}, 200)

api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
