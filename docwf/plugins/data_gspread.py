from .base import BaseDataPlugin

try:
    import gspread
    from gspread.utils import ValueRenderOption
except ModuleNotFoundError:
    # please install the gspread module to use the gspread data type
    raise


class GspreadWorkbook(BaseDataPlugin):
    """class used to read gspread workbooks"""

    def load(self):
        workbook_url = self._data_dict["workbook"]

        gc = gspread.service_account_from_dict(self._data_dict["credentials"])
        self._workbook = gc.open_by_url(workbook_url)
        # print(workbook.worksheets())
        return self
        # else:
        #     workbook = load_workbook(
        #         filename=workbook_name,
        #         data_only=True)
        # # print(workbook.sheetnames)
        # return workbook

    def get_worksheets(self):
        """
        Returns a list of worksheets
        """

        pass

    def get_column_index_map(self, sheet):
        column_index_map = {
            # cell.strip().lower(): index # cell
            cell.strip().lower(): cell
            for index, cell in enumerate(sheet.row_values(1))
            if cell
        }
        return column_index_map

    def get_value(self, sheet, row, column_index):
        return row[column_index]

    def get_worksheet(self, name):
        """returns a worksheet by name"""
        return self._workbook.worksheet(name)

    def iterrows(self, sheet):
        """iterates over the rows and gives back a index, dictionary column:value pairs"""
        for index, row in enumerate(
            sheet.get_all_records(
                empty2zero=True, value_render_option=ValueRenderOption.unformatted
            )
        ):
            # for index, row in enumerate(sheet.get_values(value_render_option=ValueRenderOption.unformatted)[1:]):
            yield (index + 2, row)


PluginClass = GspreadWorkbook
