
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