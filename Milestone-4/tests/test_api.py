import pytest
from flask import Flask
from unittest.mock import patch, MagicMock
from app import create_app, db
from app.models import Student

@pytest.fixture
def app():
    # Create Flask app for testing
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database for isolation
    with app.app_context():
        db.create_all()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

### Tests
def test_healthcheck(client):
    """Test /healthcheck endpoint"""
    response = client.get('/api/v1/healthcheck')
    assert response.status_code == 200
    assert response.get_json() == {'status': 'healthy'}

@patch('app.routes.db.session')
def test_add_student(mock_db_session, client):
    """Test POST /students endpoint"""
    mock_db_session.add = MagicMock()
    mock_db_session.commit = MagicMock()

    response = client.post('/api/v1/students', json={
        'name': 'John Doe',
        'age': 15,
        'grade': '10th'
    })

    assert response.status_code == 201
    assert 'id' in response.get_json()
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()

@patch('app.models.Student.query')
def test_get_students(mock_query, client):
    """Test GET /students endpoint"""
    mock_query.all.return_value = [
        Student(id=1, name='John Doe', age=15, grade='10th'),
        Student(id=2, name='Jane Doe', age=14, grade='9th')
    ]

    response = client.get('/api/v1/students')

    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]['name'] == 'John Doe'
    assert data[1]['grade'] == '9th'

@patch('app.models.Student.query')
def test_get_student_by_id(mock_query, client):
    """Test GET /students/<id> endpoint"""
    mock_query.get.return_value = Student(id=1, name='John Doe', age=15, grade='10th')

    response = client.get('/api/v1/students/1')

    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'John Doe'
    assert data['grade'] == '10th'

def test_get_student_not_found(client):
    """Test GET /students/<id> endpoint when student doesn't exist"""
    response = client.get('/api/v1/students/999')
    assert response.status_code == 404
    assert 'error' in response.get_json()

@patch('app.models.Student.query')
def test_delete_student(mock_query, client):
    """Test DELETE /students/<id> endpoint"""
    mock_student = Student(id=1, name='John Doe', age=15, grade='10th')
    mock_query.get.return_value = mock_student

    with patch('app.routes.db.session') as mock_db_session:
        response = client.delete('/api/v1/students/1')

        assert response.status_code == 200
        assert response.get_json() == {'message': 'Student deleted successfully'}
        mock_db_session.delete.assert_called_once_with(mock_student)
        mock_db_session.commit.assert_called_once()

@patch('app.models.Student.query')
def test_update_student(mock_query, client):
    """Test PUT /students/<id> endpoint"""
    mock_student = Student(id=1, name='John Doe', age=15, grade='10th')
    mock_query.get.return_value = mock_student

    with patch('app.routes.db.session') as mock_db_session:
        response = client.put('/api/v1/students/1', json={
            'name': 'John Updated',
            'age': 16,
            'grade': '11th'
        })

        assert response.status_code == 200
        assert response.get_json() == {'message': 'Student updated successfully'}
        assert mock_student.name == 'John Updated'
        assert mock_student.age == 16
        assert mock_student.grade == '11th'
        mock_db_session.commit.assert_called_once()
