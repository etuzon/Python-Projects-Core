import unittest

from projects.core.manager.pretty_table_manager import PrettyTableManager


class PrettyTableManagerTests(unittest.TestCase):
    HEADERS1 = ['H1', 'H2']
    ROW1 = ['R1', 'R2']

    HEADERS2 = ['H3', 'H4']
    ROW2 = ['R3', 'R4']

    TABLE_NAME = 'NAME1'
    TABLE_NAME_NOT_EXIST = 'NAME NOT EXIST'

    def test_create_table(self):  # sourcery skip: extract-duplicate-method
        """
        Test create end to end the table creation because
        table name will be different in each method.

        :return:
        """
        expected_name = 'test_create_table_NAME1'

        """
        Test create table
        """

        key = PrettyTableManager().create_table(self.HEADERS1, self.TABLE_NAME)
        self.assertTrue(key)
        self.assertTrue(
            key.find(expected_name) != -1,
            f'Table name [{key}] not contains [{expected_name}]')
        self.assertTrue(PrettyTableManager().is_table_exist(self.TABLE_NAME))

        PrettyTableManager().add_row(self.ROW1, self.TABLE_NAME)
        table = PrettyTableManager().get_table_string(self.TABLE_NAME)
        self.assertTrue(table)
        self.assertTrue(table.find(self.HEADERS1[0]) >= 0)
        self.assertTrue(table.find(self.HEADERS1[1]) >= 0)
        self.assertTrue(table.find(self.ROW1[0]) >= 0)
        self.assertTrue(table.find(self.ROW1[1]) >= 0)

        """
        Test recreate table with force_create=False
        """

        key = PrettyTableManager().create_table(
            self.HEADERS2, self.TABLE_NAME, force_create=False)
        self.assertTrue(key)
        self.assertTrue(
            key.find(expected_name) != -1,
            f'Table name [{key}] not contains [{expected_name}]')
        self.assertTrue(PrettyTableManager().is_table_exist(self.TABLE_NAME))

        table = PrettyTableManager().get_table_string(self.TABLE_NAME)
        self.assertTrue(table)
        self.assertTrue(table.find(self.HEADERS1[0]) >= 0)
        self.assertTrue(table.find(self.HEADERS1[1]) >= 0)
        self.assertTrue(table.find(self.ROW1[0]) >= 0)
        self.assertTrue(table.find(self.ROW1[1]) >= 0)

        """
        Test clear_table_rows
        """

        PrettyTableManager().clear_table_rows(self.TABLE_NAME)

        table = PrettyTableManager().get_table_string(self.TABLE_NAME)
        self.assertTrue(table)
        self.assertTrue(table.find(self.HEADERS1[0]) >= 0)
        self.assertTrue(table.find(self.HEADERS1[1]) >= 0)
        self.assertTrue(table.find(self.ROW1[0]) == -1)
        self.assertTrue(table.find(self.ROW1[1]) == -1)

        """
        Test recreate table with force_create=True
        and after that get_table_string with clear_rows=True
        """

        key = PrettyTableManager().create_table(
            self.HEADERS2, self.TABLE_NAME, force_create=True)
        self.assertTrue(key)
        self.assertTrue(
            key.find(expected_name) != -1,
            f'Table name [{key}] not contains [{expected_name}]')
        self.assertTrue(PrettyTableManager().is_table_exist(self.TABLE_NAME))

        PrettyTableManager().add_row(self.ROW2, self.TABLE_NAME)
        table = PrettyTableManager().get_table_string(
            self.TABLE_NAME, clear_rows=True)
        self.assertTrue(table)
        self.assertTrue(table.find(self.HEADERS2[0]) >= 0)
        self.assertTrue(table.find(self.HEADERS2[1]) >= 0)
        self.assertTrue(table.find(self.ROW2[0]) >= 0)
        self.assertTrue(table.find(self.ROW2[1]) >= 0)

        table = PrettyTableManager().get_table_string(
            self.TABLE_NAME)
        self.assertTrue(table)
        self.assertTrue(table.find(self.HEADERS2[0]) >= 0)
        self.assertTrue(table.find(self.HEADERS2[1]) >= 0)
        self.assertTrue(table.find(self.ROW2[0]) == -1)
        self.assertTrue(table.find(self.ROW2[1]) == -1)

    def test_is_table_exist_negative(self):
        self.assertFalse(
            PrettyTableManager().is_table_exist(self.TABLE_NAME_NOT_EXIST))

    def test_add_row_to_table_that_not_exist_negative(self):
        with self.assertRaises(Exception):
            PrettyTableManager().add_row(self.ROW1, self.TABLE_NAME_NOT_EXIST)

    def test_clear_table_row_for_table_that_not_exist_negative(self):
        with self.assertRaises(Exception):
            PrettyTableManager().clear_table_rows(self.TABLE_NAME_NOT_EXIST)

    def test_print_table_string_that_not_exist_negative(self):
        with self.assertRaises(Exception):
            PrettyTableManager().get_table_string(self.TABLE_NAME_NOT_EXIST)


if __name__ == '__main__':
    unittest.main()
