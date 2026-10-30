"""Test the frozen generic DB manager with a fake PyMySQL connection."""
import ast
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import MagicMock, patch

TEMPLATE = Path(__file__).resolve().parents[1] / 'components/templates/db-server/interface/DbMgr.py'


class DbMgrTests(unittest.TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.cursor = self.connection.cursor.return_value.__enter__.return_value
        self.cursor.fetchall.return_value = [{'ok': 1}]
        self.cursor.lastrowid = 27
        fake = types.ModuleType('pymysql')
        fake.cursors = types.ModuleType('pymysql.cursors')
        fake.cursors.DictCursor = object()
        fake.connect = MagicMock(return_value=self.connection)
        self.fake = fake
        with patch.dict(sys.modules, {'pymysql': fake, 'pymysql.cursors': fake.cursors}):
            spec = importlib.util.spec_from_file_location('test_bmforge_dbmgr', TEMPLATE)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        self.module = module
        self.config = {'host': 'localhost', 'port': 3306, 'user': 'test',
                       'password': 'secret', 'database': 'testdb'}
        self.db = module.DbMgr(**self.config)

    def test_connection_config_has_no_application_dependencies(self):
        self.assertEqual(self.fake.connect.call_args.kwargs['database'], 'testdb')
        self.assertEqual(self.fake.connect.call_args.kwargs['charset'], 'utf8mb4')
        self.assertEqual(self.fake.connect.call_args.kwargs['collation'], 'utf8mb4_unicode_ci')
        self.assertEqual(self.fake.connect.call_args.kwargs['init_command'], "SET time_zone = '+00:00'")
        self.assertTrue(self.fake.connect.call_args.kwargs['autocommit'])
        self.assertIn('STRICT_ALL_TABLES', self.fake.connect.call_args.kwargs['sql_mode'])
        self.assertEqual(self.module.BMFORGE_COMPONENT['spec_version'], '0.5.0')
        imports = set()
        for node in ast.walk(ast.parse(TEMPLATE.read_text())):
            if isinstance(node, ast.Import):
                imports.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.add(node.module)
        self.assertEqual(imports, {'contextlib', 'pymysql', 'pymysql.cursors'})

    def test_sql_methods_have_bounded_cursors(self):
        self.cursor.execute.return_value = 5
        self.cursor.executemany.return_value = 7
        self.assertEqual(self.db.execute('DELETE FROM t WHERE id=%s', (5,)), 5)
        self.assertEqual(self.db.insert('INSERT INTO t (v) VALUES (%s)', ('a',)), 27)
        self.assertEqual(self.db.execute_many('INSERT INTO t (v) VALUES (%s)', [('a',), ('b',)]), 7)
        self.assertEqual(self.db.query('SELECT 1 AS ok'), [{'ok': 1}])
        self.assertEqual(self.cursor.execute.call_args.args, ('SELECT 1 AS ok', ()))
        self.assertTrue(self.connection.cursor.return_value.__exit__.called)

    def test_transaction_commits(self):
        with self.db.transaction():
            self.db.execute('UPDATE t SET value=%s WHERE id=%s', ('a', 1))
        self.connection.begin.assert_called_once_with()
        self.connection.commit.assert_called_once_with()
        self.connection.rollback.assert_not_called()

    def test_transaction_rolls_back_and_propagates(self):
        with self.assertRaisesRegex(RuntimeError, 'failure'):
            with self.db.transaction():
                raise RuntimeError('failure')
        self.connection.rollback.assert_called_once_with()
        self.connection.commit.assert_not_called()

    def test_read_only_transaction(self):
        with self.db.transaction(read_only=True):
            self.db.query('SELECT 1 AS ok')
        self.connection.begin.assert_not_called()
        self.assertEqual(self.cursor.execute.call_args_list[0].args[0], 'START TRANSACTION READ ONLY')
        self.connection.commit.assert_called_once_with()

    def test_health_uses_the_same_connection(self):
        self.assertTrue(self.db.health())
        self.fake.connect.assert_called_once()
        self.cursor.execute.assert_called_with('SELECT 1 AS ok', ())
        self.cursor.fetchall.return_value = [{'ok': 0}]
        self.assertFalse(self.db.health())

    def test_connection_closes_with_context(self):
        with self.module.DbMgr(**self.config):
            pass
        self.connection.close.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
