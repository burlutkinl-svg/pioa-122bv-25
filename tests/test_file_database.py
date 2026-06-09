import tempfile
import unittest
from src.db.backend.file import FileDatabase
from src.db.backend.errors import (
    TableNotFoundError,
    MissingColumnError,
    UnknownColumnError,
    InvalidStorageDataError,
)

class TestFileDatabase(unittest.TestCase):
    def test_data_is_saved_between_instances(self):
        with tempfile.TemporaryDirectory() as directory:
            first_db = FileDatabase(directory)
            first_db.create_table("students", ("id", "name"))
            first_db.insert_record("students", {"id": 1, "name": "Ivan"})

            second_db = FileDatabase(directory)
            records = second_db.select_records("students")
            self.assertEqual(records, [{"id": 1, "name": "Ivan"}])

    def test_select_with_filters(self):
        with tempfile.TemporaryDirectory() as directory:
            db = FileDatabase(directory)
            db.create_table("students", ("id", "name"))
            db.insert_record("students", {"id": 1, "name": "Ivan"})
            db.insert_record("students", {"id": 2, "name": "Maria"})
            records = db.select_records("students", name="Maria")
            self.assertEqual(records, [{"id": 2, "name": "Maria"}])

    def test_select_from_missing_table(self):
        with tempfile.TemporaryDirectory() as directory:
            db = FileDatabase(directory)
            with self.assertRaises(TableNotFoundError):
                db.select_records("students")

    def test_insert_missing_column(self):
        with tempfile.TemporaryDirectory() as directory:
            db = FileDatabase(directory)
            db.create_table("students", ("id", "name"))
            with self.assertRaises(MissingColumnError):
                db.insert_record("students", {"id": 1})

    def test_insert_extra_column(self):
        with tempfile.TemporaryDirectory() as directory:
            db = FileDatabase(directory)
            db.create_table("students", ("id", "name"))
            with self.assertRaises(UnknownColumnError):
                db.insert_record("students", {"id": 1, "name": "Ivan", "age": 20})

    def test_invalid_json(self):
        with tempfile.TemporaryDirectory() as directory:
            path = FileDatabase(directory)._get_table_path("corrupt")
            path.write_text("{ not valid json", encoding="utf-8")
            db = FileDatabase(directory)
            with self.assertRaises(InvalidStorageDataError):
                db._load_table("corrupt")
