from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/staff'
db = SQLAlchemy(app)

# Configure CORS to allow requests from your Vue.js frontend
cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})
CORS(app, resources={r"/login": {"origins": "http://localhost:8080"}})

@app.route('/api/job-listings', methods=['GET'])
def get_job_listings():
    # Replace this with your database query logic
    job_listings = [
        {'title': 'Job 1', 'description': 'Description 1'},
        {'title': 'Job 2', 'description': 'Description 2'},
        # Add more job listings as needed
    ]
    return jsonify(job_listings)

# Hardcoded username and password (for demonstration purposes)
# valid_username = 'user'
# valid_password = 'password'

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')

#     if username == valid_username and password == valid_password:
#         return jsonify({"message": "Login successful"})
#     else:
#         return jsonify({"message": "Login failed"}), 401

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Query the database for the user
    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Login failed"}), 401

    
if __name__ == '__main__':
    app.run(debug=True)
