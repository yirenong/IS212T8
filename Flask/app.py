from datetime import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.orm import relationship
from sqlalchemy import func
import requests

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3308/is212'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/is212'
db = SQLAlchemy(app)

# Configure CORS to allow requests from your Vue.js frontend
cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

##################################################################################################################
### Get All Job Listings (Story #1) ###


class JobListing(db.Model):
    __tablename__ = 'Job_Listing'
    Listing_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Role_ID = db.Column(db.Integer, db.ForeignKey(
        'Role.Role_ID'), nullable=False)
    Opening = db.Column(db.Integer)
    Date_posted = db.Column(db.Date)

    role = relationship('Role', backref='job_listings')

    def to_dict(self):
        return {
            'Listing_ID': self.Listing_ID,
            'Role': {
                'Role_ID': self.role.Role_ID,
                'Role_Name': self.role.Role_Name,
                'Description': self.role.Description,
                'Department': self.role.Department,  # Include the Department field
                'Skills': [skill.Skill_Name for skill in self.role.skills]
            },
            'Opening': self.Opening,
            'Date_posted': self.Date_posted.strftime('%Y-%m-%d'),
        }


class Role(db.Model):
    __tablename__ = 'Role'
    Role_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Role_Name = db.Column(db.String(64), nullable=False)
    Description = db.Column(db.String(500), nullable=False)
    Department = db.Column(db.String(50), nullable=False)

    skills = relationship('Skill', secondary='Role_Skill')

    def to_dict(self):
        return {
            'Role_ID': self.Role_ID,
            'Role_Name': self.Role_Name,
            'Description': self.Description,
            'Department': self.Department,
            'Skills': [skill.Skill_Name for skill in self.skills]
        }


class RoleSkill(db.Model):
    __tablename__ = 'Role_Skill'
    Role_ID = db.Column(db.Integer, db.ForeignKey(
        'Role.Role_ID'), primary_key=True)
    Skill_ID = db.Column(db.Integer, db.ForeignKey(
        'Skills.Skill_ID'), primary_key=True)


# API endpoint to fetch job listings with role information and associated skills
@app.route('/api/job_list', methods=['GET'])
def get_job_listings():
    job_listings_data = JobListing.query.all()
    job_listings = [listing.to_dict() for listing in job_listings_data]

    return jsonify(job_listings)

## New code
@app.route('/api/job_list/<int:listing_id>', methods=['GET'])
def get_job_listing_by_id(listing_id):
    job_listing = JobListing.query.get(listing_id)

    if job_listing is not None:
        return jsonify(job_listing.to_dict())
    else:
        return jsonify({"error": "Job listing not found"}, 404)

##################################################################################################################
### Job Application ###

class Application(db.Model):
    __tablename__ = 'application'
    Application_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Staff_ID = db.Column(db.Integer, nullable=False)
    Listing_ID = db.Column(db.Integer, nullable=False)
    Date = db.Column(db.String, nullable=False)
    Status = db.Column(db.String, nullable=False)

    def to_dict(self):
        staff = Staff.query.filter_by(Staff_ID=self.Staff_ID).first()

        return {
            'Application_ID': self.Application_ID,
            'Listing_ID': self.Listing_ID,
            'Date': self.Date,
            'Status': self.Status,
            'Staff_ID': self.Staff_ID,
            'Staff_Name': staff.Staff_FName + " " + staff.Staff_LName,
            'Staff_Skills': [Skill.query.get(skill.Skill_ID).Skill_Name for skill in staff.skills]
        }

@app.route('/api/job_listing/<int:Staff_ID>/applications', methods=['GET'])
def get_applications_by_staff(Staff_ID):
    applications = Application.query.filter_by(Staff_ID=Staff_ID).all()
    application_data = [application.Listing_ID for application in applications]

    return jsonify(application_data)

@app.route('/api/job_listing/applications/<int:Listing_ID>/', methods=['GET'])
def get_applications_by_job(Listing_ID):
    applications = Application.query.filter_by(Listing_ID=Listing_ID).all()
    application_data = [application.to_dict() for application in applications]

    return jsonify(application_data)

@app.route('/api/job_listing/apply', methods=['POST'])
def apply():
    data = request.get_json()
    
    staff_id = data.get('Staff_ID')
    listing_id = data.get('Listing_ID')
    date = data.get('Date')
    status = data.get('Status')

    if staff_id is None or listing_id is None or date is None or status is None:
        return jsonify({'error': 'Missing required fields'}), 400

    new_application = Application(Staff_ID=staff_id, Listing_ID=listing_id, Date=date, Status=status)

    db.session.add(new_application)
    db.session.commit()

    return jsonify({'message': 'Application submitted successfully'}), 201


#########################################################################################################################
### Login ###


class Staff(db.Model):
    __tablename__ = 'staff'
    Staff_ID = db.Column(db.Integer, primary_key=True)
    Staff_FName = db.Column(db.String(50), nullable=False)
    Staff_LName = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(128), nullable=False)
    Password = db.Column(db.String(128), nullable=False)
    Dept = db.Column(db.String(50), nullable=False)
    Country = db.Column(db.String(50), nullable=False)
    Access_Rights = db.Column(db.String(50), nullable=False)
    skills = db.relationship('Staff_Skill', backref='staff')


# Inherited Class from staff
class ExtendedStaff(Staff):
    Role_ID = db.Column(db.Integer, nullable=False) 

    def __init__(self, Staff_ID, Staff_FName, Staff_LName, Email, Password, Dept, Country, Access_Rights, skills, Role_ID):
        super().__init__(Staff_ID, Staff_FName, Staff_LName, Email, Password, Dept, Country, Access_Rights, skills)
        self.Role_ID = Role_ID

@app.route('/api/staff/<int:staff_id>', methods=['GET'])
def profile(staff_id):
    staff = ExtendedStaff.query.filter_by(Staff_ID=staff_id).first()
    if not staff:
        return jsonify({'message': 'Staff not found'}), 404
    
    skills = Staff_Skill.query.filter_by(Staff_ID=staff_id).all()
    skill_names = [Skill.query.get(skill.Skill_ID).Skill_Name for skill in skills]

    staff_data = {
        'Staff_ID': staff.Staff_ID,
        'Staff_FName': staff.Staff_FName,
        'Staff_LName': staff.Staff_LName,
        'Email': staff.Email,
        'Dept': staff.Dept,
        'Country': staff.Country,
        'Access_Rights': staff.Access_Rights,
        'Role_ID': staff.Role_ID,
        'Skills': skill_names
    }

    return jsonify(staff_data), 200


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Query the database for the user
    user = Staff.query.filter_by(Staff_ID=username).first()
    if username and user.Password == password:
        userData = {
                'message': '',
                'Staff_ID': user.Staff_ID,
                'Staff_FName': user.Staff_FName,
                'Staff_LName': user.Staff_LName,
                'Dept': user.Dept,
                'Email': user.Email
            }
        if user.Dept == 'HR':
            userData['message'] = 'Management Login'

            return jsonify(userData), 200
        else:
            userData['message'] = "STAFF Login"
            return jsonify(userData), 200
    else:
        return jsonify({"message": "Login failed"}), 401

#########################################################################################################################
# SearchcandidatesbtSkills


class Skill(db.Model):
    __tablename__ = 'Skills'
    Skill_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Skill_Name = db.Column(db.String(64), nullable=False)

    def to_dict(self):
        return {
            'Skill_ID': self.Skill_ID,
            'Skill_Name': self.Skill_Name
        }


class Staff_Skill(db.Model):
    __tablename__ = 'Staff_Skill'
    Staff_ID = db.Column(db.Integer, db.ForeignKey(
        'staff.Staff_ID'), primary_key=True)
    Skill_ID = db.Column(db.Integer, db.ForeignKey(
        'Skills.Skill_ID'), primary_key=True)

    def to_dict(self):
        return {
            'Staff_ID': self.Staff_ID,
            'Skill_ID': self.Skill_ID
        }

@app.route('/api/skill/', methods=['GET'])
def get_skill():
    skill_data = Skill.query.all()
    skill_list = [skill.to_dict() for skill in skill_data]

    return jsonify(skill_list)

@app.route('/api/skill' , methods=['POST'])
def add_skill():
    data = request.get_json()
    skill_name = data.get('Skill_Name')

    if not skill_name:
        return jsonify({'message': 'Skill name is required'}), 400

    new_skill = Skill(Skill_Name=skill_name)
    db.session.add(new_skill)
    db.session.commit()

    return jsonify({'message': 'Skill added successfully'}), 201

@app.route('/api/search_staff_by_skill', methods=['POST'])
def search_staff_by_skill():
    userrequest = request.get_json()
    datalist = userrequest.get('selected')
    exactmatch = userrequest.get('exactmatch')

    numbersofskills = len(datalist)-1 if exactmatch == 1 else 1
    print(numbersofskills)
    staff_skillslist =Staff_Skill.query.filter(Staff_Skill.Skill_ID.in_(datalist)).group_by(Staff_Skill.Staff_ID).having(func.count(Staff_Skill.Skill_ID) >numbersofskills).with_entities(Staff_Skill.Staff_ID).all()
    staff_id = [staff[0] for staff in staff_skillslist]

    staff_list = Staff.query.filter(Staff.Staff_ID.in_(staff_id)).all()
    skill_list = Staff_Skill.query.filter(Staff_Skill.Staff_ID.in_(staff_id)).all()
    
    staff_data = []
    for staff in staff_list:
        staff_data.append({
            'Staff_ID': staff.Staff_ID,
            'Staff_FName': staff.Staff_FName,
            'Staff_LName': staff.Staff_LName,
            'Dept': staff.Dept,
            'Skills': [skill.Skill_ID for skill in skill_list if skill.Staff_ID == staff.Staff_ID]
        })
    return jsonify(staff_data)
    
    # return jsonify(staff_skillslist)

## role skill
@app.route('/api/update_role_skills', methods=['POST'])
def update_role_skills():
    data = request.get_json()
    role_id = data.get('role_id')
    skill_ids = data.get('skill_ids')

    if not role_id or not skill_ids:
        return jsonify({'message': 'Both role_id and skill_ids are required'}), 400

    try:
        # Add/update role skills
        for skill_id in skill_ids:
            new_role_skill = RoleSkill(Role_ID=role_id, Skill_ID=skill_id)
            db.session.add(new_role_skill)

        db.session.commit()
        return jsonify({'message': 'Role skills updated successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating role skills', 'error': data}, ), 500
    finally:
        db.session.close()

@app.route('/api/skill_list', methods=['GET'])
def get_skill_list():
    skill_list_data = Skill.query.all()
    skill_list = [skill.to_dict() for skill in skill_list_data]

    return jsonify(skill_list)


@app.route('/api/staff_skill', methods=['GET'])
def get_staff_skill():
    staff_skill_data = Staff_Skill.query.all()
    staff_list = Staff.query.all()
    # only get staff_ID, fname, lname,dept from staff table
    staff_skill = []
    for staff in staff_list:
        staff_skill.append({
            'Staff_ID': staff.Staff_ID,
            'Staff_FName': staff.Staff_FName,
            'Staff_LName': staff.Staff_LName,
            'Dept': staff.Dept,
            'Skills': [skill.Skill_ID for skill in staff_skill_data if skill.Staff_ID == staff.Staff_ID]
        })

    return jsonify(staff_skill)

##################################################################################################################
### Maintain Job Listing (Story #2) ###
# Create new job listing
@app.route('/api/job_list/new', methods=['POST'])
def new_job_listing():
    data = request.get_json()
    job_listing = JobListing(Listing_ID = JobListing.query.count() + 1,
                            Role_ID=data.get('Role_ID'),
                            Opening=data.get('Opening'),
                            Date_posted=datetime.strptime(data.get('Date_posted'), '%Y-%m-%d'))

    db.session.add(job_listing)
    db.session.commit()
    return jsonify(job_listing.to_dict()), 200

# Create new role
@app.route('/api/roles/new', methods=['POST'])
def new_role():
    data = request.get_json()
    new_role = Role(Role_ID = Role.query.count() + 1,
                    Role_Name=data.get('Role_Name'),
                    Description=data.get('Description'),
                    Department=data.get('Department'))
    db.session.add(new_role)
    
    for skillName in data.get('Skills'):
        skill = Skill.query.filter_by(Skill_Name=skillName).first()
        
        if not skill:
            # Create a new skill if it doesn't exist
            new_skill = Skill(Skill_Name=skillName)
            db.session.add(new_skill)
            db.session.commit()
            
            skill = Skill.query.filter_by(Skill_Name=skillName).first()
        
        new_role_skill = RoleSkill(Role_ID=new_role.Role_ID, Skill_ID=skill.Skill_ID)
        db.session.add(new_role_skill)
    
    db.session.commit()

    return jsonify(new_role.to_dict()), 200

@app.route('/api/roles', methods=['GET'])
def get_all_roles():
    roles = Role.query.all()
    role_data = [role.to_dict() for role in roles]
    return jsonify(role_data)

@app.route('/api/roles/<int:role_id>', methods=['GET'])
def get_role_by_id(role_id):
    role = Role.query.get(role_id)
    if not role:
        return jsonify({'message': 'Role not found'}), 404

    role_data = role.to_dict()
    return jsonify(role_data), 200


@app.route('/api/roles/<int:role_id>', methods=['PUT'])
def update_role(role_id):
    data = request.get_json()
    role_name = data.get('Role_Name')
    description = data.get('Description')
    department = data.get('Department')

    role = Role.query.get(role_id)

    if role is None:
        return jsonify({'message': 'Role not found'}), 404

    role.Role_Name = role_name
    role.Description = description
    role.Department = department

    db.session.commit()

    response = requests.put(f'http://localhost:5000/api/staff/update-department/{role_id}/{department}')

    if response.status_code == 200:
        return jsonify(role.to_dict())
    else:
        return jsonify({'message': 'Failed to update staff department'}), 500

@app.route('/api/staff/update-department/<int:role_id>/<new_department>', methods=['PUT'])
def update_staff_department(role_id, new_department):
    # Find all staff members with the specified role ID
    staff_to_update = ExtendedStaff.query.filter(ExtendedStaff.Role_ID == role_id).all()

    if not staff_to_update:
        return jsonify({'message': 'No staff members found with the specified role ID'}), 200

    for staff in staff_to_update:
        staff.Dept = new_department

    db.session.commit()

    return jsonify({'message': 'Department updated for staff members with role ID {}'.format(role_id)}), 200



@app.route('/api/job_list/<int:listing_id>', methods=['PUT'])
def update_job_listing(listing_id):
    data = request.get_json()

    role_name = data.get('Role_Name')
    opening = data.get('Opening')

    job_listing = JobListing.query.get(listing_id)

    if job_listing is None:
        return jsonify({'message': 'Job listing not found'}), 404

    role = Role.query.filter_by(Role_Name=role_name).first()
    if role is None:
        return jsonify({'message': 'Role not found'}), 404

    job_listing.Role_ID = role.Role_ID
    job_listing.Opening = opening

    db.session.commit()

    return jsonify(job_listing.to_dict()), 200


##################################################################################################################
### Staff Skills ###
@app.route('/api/staff_skill/<int:staff_id>', methods=['GET'])
def get_staff_skill_by_id(staff_id):
    # Get staff details for the given staff_id
    staff = Staff.query.filter_by(Staff_ID=staff_id).first()

    if not staff:
        return jsonify({'message': 'Staff not found'}), 404

    # Get skills for the given staff_id and fetch their names
    staff_skills = (
        db.session.query(Skill)
        .join(Staff_Skill, Skill.Skill_ID == Staff_Skill.Skill_ID)
        .filter(Staff_Skill.Staff_ID == staff_id)
        .all()
    )
    
    skill_names = [skill.Skill_Name for skill in staff_skills]

    staff_skill_data = {
        'Staff_ID': staff.Staff_ID,
        'Staff_FName': staff.Staff_FName,
        'Staff_LName': staff.Staff_LName,
        'Dept': staff.Dept,
        'Skills': skill_names 
    }

    return jsonify(staff_skill_data), 200


##################################################################################################################
### Staff applied job ###

@app.route('/api/staff/staff_app/<int:staff_id>', methods=['GET'])
def get_data(staff_id): 
    applications = Application.query.filter_by(Staff_ID=staff_id).all()
    applied_listing_ids = [app.Listing_ID for app in applications]
    listings = JobListing.query.filter(JobListing.Listing_ID.in_(applied_listing_ids)).all()
    
    application_data = [
        {
            "application_id": app.Application_ID,
            "staff_id": app.Staff_ID,
            "listing_id": app.Listing_ID,
            "status": app.Status
        } for app in applications
    ]
    
    listing_data = [
        {
            "listing_id": listing.Listing_ID,
            "role_id": listing.Role_ID
        } for listing in listings
    ]

    role_ids = [listing.Role_ID for listing in listings]
    roles = Role.query.filter(Role.Role_ID.in_(role_ids)).all()
    
    role_data = [
        {
            "role_id": role.Role_ID,
            "role_name": role.Role_Name,
            "description": role.Description,
            "department": role.Department
        } for role in roles
    ]
    
    return jsonify({
        "applications": application_data,
        "listings": listing_data,
        "roles": role_data
    })






if __name__ == '__main__':
    app.run(debug=True)
