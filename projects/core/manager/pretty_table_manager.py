import ntpath
from inspect import stack

from prettytable import PrettyTable


class PrettyTableManager:

    _pretty_table_dict: dict[str, PrettyTable] = {}
    _align: str = 'l'

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = cls._instance = \
                super(PrettyTableManager, cls).__new__(cls, *args, **kwargs)

        return cls._instance

    def create_table(
            self,
            headers: list,
            table_name: str = '',
            force_create: bool = True,
            sub_method_level: int = 0) -> str:
        key, table = self._get_key_and_table(table_name, sub_method_level)

        if force_create or not table:
            self._pretty_table_dict[key] = \
                PrettyTable(field_names=headers, align=self.align)

        return key

    def is_table_exist(
            self, table_name: str = '', sub_method_level: int = 0) -> bool:
        return bool(self._get_key_and_table(table_name, sub_method_level)[1])

    def add_row(
            self, row: list, table_name: str = '', sub_method_level: int = 0):
        key, table = self._get_key_and_table(table_name, sub_method_level)

        if not table:
            raise Exception(
                f'Bug: PrettyTable [{key}] not exists')

        table.add_row(row)

    def clear_table_rows(
            self, table_name: str = '', sub_method_level: int = 0):
        key, table = self._get_key_and_table(table_name, sub_method_level)

        if not table:
            raise Exception(
                f'Bug: PrettyTable [{key}] not exists')

        table.clear_rows()

    def get_table_string(
            self,
            table_name: str = '',
            clear_rows: bool = False,
            sub_method_level: int = 0) -> str:
        key, table = self._get_key_and_table(table_name, sub_method_level)

        if not table:
            raise Exception(
                f'Bug: PrettyTable [{key}] not exist')

        table_str = table.get_string()

        if clear_rows:
            table.clear_rows()

        return table_str

    def _get_key_and_table(
            self,
            table_name: str,
            sub_method_level: int = 0) -> tuple[str, PrettyTable]:
        key = self._get_table_key(table_name, sub_method_level)
        return key, self._pretty_table_dict.get(key)

    @classmethod
    def _get_table_key(cls, name: str, sub_method_level: int = 0):
        s = stack()
        row_index = 3 + sub_method_level
        function_name = s[row_index][3]
        file_name = ntpath.basename(s[row_index][1])
        return f'{file_name}_{function_name}_{name}'

    @property
    def align(self):
        return self._align

    @align.setter
    def align(self, align: str):
        self._align = align
