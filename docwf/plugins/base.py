
class BasePlugin():

    def __init__(self, task_helper, task_info, globals_dict, *args, **kwargs):
        self._task_helper = task_helper
        self._globals_dict = globals_dict
        self._task_info = task_info

    def do_task(self, task_params, **kwargs):
        """
        does the task for one row of data 

        task_params are the preprocessed row data and constants as per the task definition
        row is the raw data from the source
        """
        pass

    def finish(self):
        pass

class BaseDataPlugin():

    def __init__(self, data_dict, *args, **kwargs):
        self._data_dict = data_dict
        self._workbook = None

    def load(self):
        """loads the workbook"""
        pass

    def get_worksheets(self):
        """
        Returns a list of worksheets
        """
        pass

    def get_worksheet(self, name):
        """returns a worksheet by name"""

    def get_column_index_map(self, sheet):
        """ returns a mapping of column name (lower) : index for a row to get the value """

    def get_value(self, sheet, row, column_index):
        """ returns a value from a row of the sheet with an index """

    def iterrows(self, worksheet):
        """iterates over the rows and gives back a dictionary column:value"""
        yield from ()

    def finish(self):
        pass