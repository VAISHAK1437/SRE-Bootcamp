from flask import Blueprint, jsonify, request
from .models import Student, db

api_bp = Blueprint('api', __name__)

@api_bp.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    student = Student(name=data['name'], age=data['age'], grade=data['grade'])
    db.session.add(student)
    db.session.commit()
    return jsonify({'id': student.id}), 201

@api_bp.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([{'id': s.id, 'name': s.name, 'age': s.age, 'grade': s.grade} for s in students])

@api_bp.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get_or_404(id)
    return jsonify({'id': student.id, 'name': student.name, 'age': student.age, 'grade': student.grade})

@api_bp.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()
    student = Student.query.get_or_404(id)
    student.name = data['name']
    student.age = data['age']
    student.grade = data['grade']
    db.session.commit()
    return jsonify({'message': 'Student updated successfully'})

@api_bp.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted successfully'})

@api_bp.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({'status': 'healthy'})

# Handle favicon requests
@api_bp.route('/favicon.ico')
def favicon():
    return '', 204


