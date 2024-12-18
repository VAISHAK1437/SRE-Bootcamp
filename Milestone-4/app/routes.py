from flask import Blueprint, jsonify, request
from .models import Student, db

api_bp = Blueprint("api", __name__)


@api_bp.route("/students", methods=["POST"])
def add_student():
    """Add a new student."""
    data = request.get_json()
    if not data or "name" not in data or "age" not in data or "grade" not in data:
        return jsonify({
            "error": "Missing required fields"
        }), 400

    student = Student(
        name=data["name"],
        age=data["age"],
        grade=data["grade"]
    )
    db.session.add(student)
    db.session.commit()
    return jsonify({"id": student.id}), 201


@api_bp.route("/students", methods=["GET"])
def get_students():
    """Get a list of all students."""
    students = Student.query.all()
    return jsonify([
        {"id": s.id, "name": s.name, "age": s.age, "grade": s.grade}
        for s in students
    ])


@api_bp.route("/students/<int:id>", methods=["GET"])
def get_student(id):
    """Get a specific student by ID."""
    student = Student.query.get(id)
    if not student:
        return jsonify({
            "error": f"Student with id {id} not found"
        }), 404

    return jsonify({
        "id": student.id,
        "name": student.name,
        "age": student.age,
        "grade": student.grade
    })


@api_bp.route("/students/<int:id>", methods=["PUT"])
def update_student(id):
    """Update an existing student's information."""
    data = request.get_json()
    if not data or "name" not in data or "age" not in data or "grade" not in data:
        return jsonify({
            "error": "Missing required fields"
        }), 400

    student = Student.query.get(id)
    if not student:
        return jsonify({
            "error": f"Student with id {id} not found"
        }), 404

    student.name = data["name"]
    student.age = data["age"]
    student.grade = data["grade"]
    db.session.commit()
    return jsonify({"message": "Student updated successfully"})


@api_bp.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    """Delete a specific student by ID."""
    student = Student.query.get(id)
    if not student:
        return jsonify({
            "error": f"Student with id {id} not found"
        }), 404

    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted successfully"})


@api_bp.route("/healthcheck", methods=["GET"])
def healthcheck():
    """Check the health of the application."""
    return jsonify({"status": "healthy"})
