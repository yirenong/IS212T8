from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/staff'
db = SQLAlchemy(app)

# Configure CORS to allow requests from your Vue.js frontend
cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})
CORS(app, resources={r"/login": {"origins": "http://localhost:8080"}})

#Class for joblisting and retrieve it from MYSQL
class JobListing(db.Model):
    __tablename__ = 'job_listing'
    Listing_ID = db.Column(db.Integer, primary_key=True)
    Role_ID  = db.Column(db.Integer, nullable=False)
    Opening  = db.Column(db.Integer)
    Date_posted = db.Column(db.Date)

#getting from the class above and send it to vue
@app.route('/api/job-listings', methods=['GET'])
def get_job_listings():
    job_listings_data = JobListing.query.all()
    job_listings = [{
        'Listing_ID': listing.Listing_ID,
        'Role_ID': listing.Role_ID,
        'Opening': listing.Opening,
        'Date_posted': listing.Date_posted.strftime('%Y-%m-%d'),
    } for listing in job_listings_data]

    return jsonify(job_listings)

class Staff(db.Model):
    __tablename__ = 'staff'
    Staff_ID = db.Column(db.Integer, primary_key=True)
    Staff_FName = db.Column(db.String(50), nullable=False)
    Staff_LName = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(128), nullable=False)
    Password = db.Column(db.String(128), nullable=False)
    Dept = db.Column(db.String(50), nullable=False)
    Country = db.Column(db.String(50), nullable=False)
    Access_Level = db.Column(db.String(50), nullable=False)


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Query the database for the user
    user = Staff.query.filter_by(Staff_ID=username).first()

    if user and user.Password == password:
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Login failed"}), 401

    
if __name__ == '__main__':
    app.run(debug=True)
