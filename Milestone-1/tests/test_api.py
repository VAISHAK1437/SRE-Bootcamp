import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from app import create_app, db
from app.models import Student

class StudentAPITestCase(unittest.TestCase):
    def setUp(self):
        """Setup the test environment."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_student(self):
        """Test adding a student."""
        response = self.client.post('/api/v1/students', json={
            'name': 'John Doe',
            'age': 20,
            'grade': 'A'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    def test_get_students(self):
        """Test getting all students."""
        # First, add a student
        self.client.post('/api/v1/students', json={
            'name': 'John Doe',
            'age': 20,
            'grade': 'A'
        })
        
        response = self.client.get('/api/v1/students')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json), 0)  # Should return at least one student

    def test_get_student(self):
        """Test getting a single student by ID."""
        # Add a student first
        student = self.client.post('/api/v1/students', json={
            'name': 'John Doe',
            'age': 20,
            'grade': 'A'
        })
        student_id = student.json['id']

        response = self.client.get(f'/api/v1/students/{student_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], student_id)
        self.assertEqual(response.json['name'], 'John Doe')

    def test_get_student_not_found(self):
        """Test getting a student that doesn't exist."""
        response = self.client.get('/api/v1/students/999')
        self.assertEqual(response.status_code, 404)

    def test_update_student(self):
        """Test updating a student's information."""
        # Add a student
        student = self.client.post('/api/v1/students', json={
            'name': 'John Doe',
            'age': 20,
            'grade': 'A'
        })
        student_id = student.json['id']

        # Update the student's information
        response = self.client.put(f'/api/v1/students/{student_id}', json={
            'name': 'Jane Doe',
            'age': 22,
            'grade': 'B'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Student updated successfully')

        # Verify the update
        response = self.client.get(f'/api/v1/students/{student_id}')
        self.assertEqual(response.json['name'], 'Jane Doe')
        self.assertEqual(response.json['age'], 22)
        self.assertEqual(response.json['grade'], 'B')

    def test_delete_student(self):
        """Test deleting a student."""
        # Add a student
        student = self.client.post('/api/v1/students', json={
            'name': 'John Doe',
            'age': 20,
            'grade': 'A'
        })
        student_id = student.json['id']

        # Delete the student
        response = self.client.delete(f'/api/v1/students/{student_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Student deleted successfully')

        # Verify the student is deleted
        response = self.client.get(f'/api/v1/students/{student_id}')
        self.assertEqual(response.status_code, 404)

    def test_healthcheck(self):
        """Test the healthcheck endpoint."""
        response = self.client.get('/api/v1/healthcheck')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'healthy')

if __name__ == '__main__':
    unittest.main()
