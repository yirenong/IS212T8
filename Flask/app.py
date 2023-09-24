from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

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
valid_username = 'user'
valid_password = 'password'

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username == valid_username and password == valid_password:
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Login failed"}), 401
    
if __name__ == '__main__':
    app.run(debug=True)
