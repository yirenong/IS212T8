# test/unittest.py
import unittest
from unittest.mock import patch, MagicMock
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
        self.app_context = app.app_context()  # Create an application context
        self.app_context.push()  # Push the application context

        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory SQLite database for testing
        db.create_all()  # Create database schema in memory
        self.client = app.test_client()

        self.mock_job_listing = MagicMock()
        self.mock_job_listing.to_dict.return_value = mock_job_listing_dict

        # Patch db.session.query to use a MagicMock
        self.mock_query = MagicMock()
        self.mock_query.all.return_value = [self.mock_job_listing]
        self.mock_query.get.return_value = self.mock_job_listing
        self.query_patch = patch('Flask.app.db.session.query', MagicMock(return_value=self.mock_query))
        self.query_patch.start()

    def tearDown(self):
        """Tear down all initialized variables."""
        db.session.remove()
        db.drop_all()  # Drop all data after each test
        self.query_patch.stop()  # Stop patching
        self.app_context.pop()  # Pop the application context

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
