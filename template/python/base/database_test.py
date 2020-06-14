import unittest
from database import Database
from unittest.mock import Mock, call

class DatabaseTest(unittest.TestCase):

    def setUp(self):
        self.db = Mock()
        self.db.cursor = Mock()
        self.db.cursor.execute = Mock(return_value=None)

    def test_query(self):
        result = Database.query(self.db, 'SELECT 1')
        self.assertEqual(result, self.db.cursor)
        self.db.cursor.execute.assert_called_once()

    def test_first(self):
        self.db.query = Mock(return_value=self.db.cursor)
        Database.first(self.db, 'SELECT 1')
        self.db.cursor.fetchone.assert_called_once()

    def test_all(self):
        self.db.query = Mock(return_value=self.db.cursor)
        Database.all(self.db, 'SELECT 1')
        self.db.cursor.fetchall.assert_called_once()

    def test_find(self):
        sql = 'SELECT * FROM table WHERE id = %s AND field = %s'\
            ' ORDER BY id DESC LIMIT 1'
        Database.find(self.db, 'table', id=1, field='abc')
        self.db.first.assert_called_once()
        self.assertEqual(call(sql, 1, 'abc'), self.db.first.call_args)
