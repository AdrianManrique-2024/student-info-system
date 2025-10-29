import json
import os
from datetime import datetime
from ..models.student import Student

class StudentService:
    def __init__(self, data_file='data/students.json'):
        self.data_file = data_file
        self._ensure_data_file()

    def _ensure_data_file(self):
        dir_name = os.path.dirname(self.data_file)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def _load_students(self):
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_students(self, students):
        tmp_path = f"{self.data_file}.tmp"
        with open(tmp_path, 'w', encoding='utf-8') as f:
            json.dump(students, f, indent=2, ensure_ascii=False)
        os.replace(tmp_path, self.data_file)

    def add_student(self, student_data):
        students = self._load_students()
        student = Student(**student_data)
        students.append(student.to_dict())
        self._save_students(students)
        return student.to_dict()

    def get_all_students(self):
        return self._load_students()

    def get_student(self, student_id):
        students = self._load_students()
        for student in students:
            if student.get('student_id') == student_id:
                return student
        return None

    def update_student(self, student_id, update_data):
        students = self._load_students()
        for student in students:
            if student.get('student_id') == student_id:
                student.update(update_data)
                student['updated_at'] = datetime.now().isoformat()
                self._save_students(students)
                return student
        return None

    def delete_student(self, student_id):
        students = self._load_students()
        original_len = len(students)
        students = [s for s in students if s.get('student_id') != student_id]
        if len(students) == original_len:
            return False
        self._save_students(students)
        return True
