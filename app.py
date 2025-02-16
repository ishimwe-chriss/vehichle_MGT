from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicles.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

# Initialize database
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    vehicles = Vehicle.query.all()
    return render_template('index.html', vehicles=vehicles)

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([{ 'id': v.id, 'make': v.make, 'model': v.model, 'year': v.year, 'price': v.price } for v in vehicles])

@app.route('/vehicles', methods=['POST'])
def add_vehicle():
    data = request.json
    new_vehicle = Vehicle(make=data['make'], model=data['model'], year=data['year'], price=data['price'])
    db.session.add(new_vehicle)
    db.session.commit()
    return jsonify({'message': 'Vehicle added successfully'}), 201

@app.route('/vehicles/<int:id>', methods=['PUT'])
def update_vehicle(id):
    data = request.json
    vehicle = Vehicle.query.get(id)
    if not vehicle:
        return jsonify({'message': 'Vehicle not found'}), 404
    
    vehicle.make = data['make']
    vehicle.model = data['model']
    vehicle.year = data['year']
    vehicle.price = data['price']
    db.session.commit()
    return jsonify({'message': 'Vehicle updated successfully'})

@app.route('/vehicles/<int:id>', methods=['DELETE'])
def delete_vehicle(id):
    vehicle = Vehicle.query.get(id)
    if not vehicle:
        return jsonify({'message': 'Vehicle not found'}), 404
    
    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({'message': 'Vehicle deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
