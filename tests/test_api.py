import unittest
from app import create_app, db
from app.models import Student

class StudentAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_student(self):
        response = self.client.post('/api/v1/students', json={
            'name': 'John Doe',
            'age': 20,
            'grade': 'A'
        })
        self.assertEqual(response.status_code, 201)

    def test_get_students(self):
        response = self.client.get('/api/v1/students')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
