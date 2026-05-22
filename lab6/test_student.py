from pathlib import Path
import pytest
import csv

class FileStructureError(Exception):
    pass

class InvalidStudentDataError(Exception):
    pass

class EmptyFileError(Exception):
    pass

class StudentRecord:
    def __init__(self, id, name, grade):
        self.id = id
        self.name = name
        self.grade = grade

    def student_info(self):
        print(f"-----Student info----- \nID => {self.id}\nName => {self.name}\nGrade => {self.grade}")

def validate_id(id_val):
    if not isinstance(id_val, int):
        raise InvalidStudentDataError("ID musi byc typu int")
    if id_val < 1: 
        raise InvalidStudentDataError("ID musi byc dodatanie")
    return True

def validate_name(name):
    if not isinstance(name, str):
        raise InvalidStudentDataError("Imie musi byc typu string")
    if name.strip() == "":
        raise InvalidStudentDataError("Imie nie moze byc puste")
    return True

def validate_grade(grade_val):
    if not isinstance(grade_val, float):
        raise InvalidStudentDataError("Ocena musi byc typu float")
    if not (2.0 <= grade_val <= 5.0):
        raise InvalidStudentDataError("Ocena musi byc z przedzialu od 2.0 do 5.0")
    return True

def validate_student(id_val, name, grade_val):
    return validate_id(id_val) and validate_name(name) and validate_grade(grade_val)

def load_students(path):
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError("Plik nie istnieje")

    student_list = []

    with open(path, mode='r', encoding='utf-8') as file:
        info = csv.reader(file)

        try:
            head = next(info) 
        except StopIteration:
            raise EmptyFileError("Plik jest pusty.")

        for line in info:
            if len(line) != 3:
                raise FileStructureError("Brakujace dane w pliku csv")

            try:
                converted_id = int(line[0])
                converted_grade = float(line[2])
                name = line[1]
            except ValueError:
                raise InvalidStudentDataError("Niepoprawny format typu danych w CSV")

            if validate_student(converted_id, name, converted_grade):
                student = StudentRecord(converted_id, name, converted_grade)
                student_list.append(student)

    return student_list




def test_load_students_correct_data(tmp_path):
    file_path = tmp_path / "students_correct.csv"
    file_path.write_text("id,name,grade\n1,Jan Kowalski,4.5\n2,Anna Nowak,5.0", encoding="utf-8")

    students = load_students(file_path)

    assert len(students) == 2
    assert students[0].id == 1
    assert students[0].name == "Jan Kowalski"
    assert students[0].grade == 4.5



def test_load_students_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_students("xyz.csv")


def test_load_students_empty_file(tmp_path):
    file_path = tmp_path / "empty.csv"
    file_path.write_text("", encoding="utf-8") 

    with pytest.raises(EmptyFileError):
        load_students(file_path)


def test_load_students_missing_column(tmp_path):
    file_path = tmp_path / "missing_column.csv"
    file_path.write_text("id,name,grade\n1,Jan Kowalski", encoding="utf-8")

    with pytest.raises(FileStructureError):
        load_students(file_path)


def test_load_students_invalid_data_type(tmp_path):
    file_path = tmp_path / "invalid_type.csv"
    file_path.write_text("id,name,grade\nXYZ,Jan Kowalski,4.5", encoding="utf-8")

    with pytest.raises(InvalidStudentDataError):
        load_students(file_path)


def test_load_students_grade_out_of_range(tmp_path):
    file_path = tmp_path / "grade_out_of_range.csv"
    file_path.write_text("id,name,grade\n1,Jan Kowalski,6.0", encoding="utf-8")

    with pytest.raises(InvalidStudentDataError):
        load_students(file_path)


def test_load_students_empty_record(tmp_path):
    file_path = tmp_path / "empty_record.csv"
    file_path.write_text("id,name,grade\n,,", encoding="utf-8")

    with pytest.raises(FileStructureError):
        load_students(file_path)
