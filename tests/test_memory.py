import unittest
import os
import json
from src.db.backend.memory import Table

class TestTable(unittest.TestCase):
    def setUp(self):
        self.name = "test_table"
        self.filename = f"{self.name}.json"
        if os.path.exists(self.filename):
            os.remove(self.filename)
        self.table = Table(self.name)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_initialization(self):
        self.assertEqual(self.table.name, self.name)
        self.assertEqual(self.table.data, {})
        self.assertIsNone(self.table.sort_order)

    def test_write_new_key(self):
        self.table.write("key1", "hello world")
        self.assertIn("key1", self.table.data)
        self.assertEqual(self.table.data["key1"], ["hello", "world"])

    def test_write_existing_key(self):
        self.table.write("key1", "a b")
        self.table.write("key1", "c d")
        self.assertEqual(self.table.data["key1"], ["a", "b", "c", "d"])

    def test_read_no_filters(self):
        self.table.write("b", "b1")
        self.table.write("a", "a1")
        records = self.table.read()
        self.assertEqual(list(records.keys()), ["b", "a"])
        self.assertEqual(records["b"], ["b1"])
        self.assertEqual(records["a"], ["a1"])

    def test_read_with_filters(self):
        self.table.write("a", "1")
        self.table.write("b", "2")
        self.table.write("c", "3")
        records = self.table.read(["a", "c"])
        self.assertEqual(list(records.keys()), ["a", "c"])

    def test_read_filter_nonexistent(self):
        self.table.write("a", "1")
        records = self.table.read(["x"])
        self.assertEqual(records, {})

    def test_delete_one_key(self):
        self.table.write("a", "1")
        self.table.write("b", "2")
        self.table.delete(["a"])
        self.assertNotIn("a", self.table.data)
        self.assertIn("b", self.table.data)

    def test_delete_multiple_keys(self):
        self.table.write("a", "1")
        self.table.write("b", "2")
        self.table.write("c", "3")
        self.table.delete(["a", "c"])
        self.assertNotIn("a", self.table.data)
        self.assertNotIn("c", self.table.data)
        self.assertIn("b", self.table.data)

    def test_set_sort_asc(self):
        self.table.write("b", "1")
        self.table.write("a", "2")
        self.table.set_sort("asc")
        records = self.table.read()
        self.assertEqual(list(records.keys()), ["a", "b"])

    def test_set_sort_desc(self):
        self.table.write("a", "1")
        self.table.write("b", "2")
        self.table.set_sort("desc")
        records = self.table.read()
        self.assertEqual(list(records.keys()), ["b", "a"])

    def test_set_sort_none(self):
        self.table.write("b", "1")
        self.table.write("a", "2")
        self.table.set_sort(None)
        records = self.table.read()
        self.assertEqual(list(records.keys()), ["b", "a"])

    def test_persistence(self):
        self.table.write("key", "persist")
        self.table = Table(self.name)  # reload
        self.assertIn("key", self.table.data)
        self.assertEqual(self.table.data["key"], ["persist"])

if __name__ == "__main__":
    unittest.main()
