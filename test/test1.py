# test/unittest.py
import unittest
from unittest.mock import MagicMock
from flask import json
from Flask.app import app, db

# Assuming this is the structure you want to test with
mock_job_listing_dict = {
    'Listing_ID': 1,
    'Role': {
        'Role_ID': 1,
        'Role_Name': 'Software Developer',
        'Description': 'Develop applications.',
        'Department': 'Engineering',
        'Skills': ['Python', 'Flask']
    },
    'Opening': 3,
    'Date_posted': '2023-01-01'
}

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        """Set up test client and other test variables."""
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Mock the database session query
        self.mock_job_listing = MagicMock()
        self.mock_job_listing.to_dict.return_value = mock_job_listing_dict
        db.session.query.return_value.all.return_value = [self.mock_job_listing]
        db.session.query.return_value.get.return_value = self.mock_job_listing

    def tearDown(self):
        """Tear down all initialized variables."""
        self.app_context.pop()

    def test_get_job_listings(self):
        """Test API can get job listings."""
        response = self.client.get('/api/job_list')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data, [mock_job_listing_dict])

    def test_get_job_listing_by_id(self):
        """Test API can get a single job listing by its ID."""
        response = self.client.get('/api/job_list/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data, mock_job_listing_dict)

if __name__ == '__main__':
    unittest.main()
