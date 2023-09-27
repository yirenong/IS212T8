from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/staff'
db = SQLAlchemy(app)

# Configure CORS to allow requests from your Vue.js frontend
cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})
CORS(app, resources={r"/login": {"origins": "http://localhost:8080"}})

class JobListing(db.Model):
    __tablename__ = 'joblistings'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255))
    location = db.Column(db.String(255))
    description = db.Column(db.Text)
    posted_date = db.Column(db.Date)
    salary = db.Column(db.Numeric(10, 2))
    contact_email = db.Column(db.String(255))

@app.route('/api/job-listings', methods=['GET'])
def get_job_listings():
    job_listings_data = JobListing.query.all()
    job_listings = [{
        'id': listing.id,
        'title': listing.title,
        'company': listing.company,
        'location': listing.location,
        'description': listing.description,
        'posted_date': listing.posted_date.strftime('%Y-%m-%d'),
        'salary': float(listing.salary) if listing.salary is not None else None,
        'contact_email': listing.contact_email,
    } for listing in job_listings_data]

    return jsonify(job_listings)

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
