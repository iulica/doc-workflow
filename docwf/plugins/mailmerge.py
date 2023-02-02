""" mailmerge plugin - mailmerge a docx """

from .base import BasePlugin
from mailmerge import MailMerge

class MailMergeTask(BasePlugin):

    """ class used for the docx mailmerge task """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert 'sheet' in kwargs and 'workbook' in kwargs
        self._rows = []
        self._document = None
        self._fields = None
        self._output_filename = None
        self._workbook = kwargs['workbook']
        self._sheet = kwargs['sheet']
        self._column_map = {
            column_name.replace(' ', '_'): column_index
            for column_name, column_index in self._workbook.get_column_index_map(
                self._sheet).items()
        }

    def _init_document(self, value_dict):
        input_docx_filename = self._task_info['input_docx'].format(**value_dict)
        self._document = MailMerge(input_docx_filename, auto_update_fields_on_open="auto")
        self._fields = self._document.get_merge_fields()
        self._output_filename = self._task_info['output_docx'].format(**value_dict)
        
    def do_task(self, value_dict, **kwargs):
        assert 'row' in kwargs
        row = kwargs['row']

        if self._document is None:
            self._init_document(value_dict)

        data_dict = {
            field_name: self._workbook.get_value(self._sheet, row, self._column_map[field_name.lower()])
            for field_name in self._fields
        }
        # print(data_dict)

        self._rows.append(data_dict)
    
    def finish(self):

        # print(merge_data)
        separator = self._task_info.get('separator', 'page_break')
        self._document.merge_templates(self._rows, separator=separator)
        self._document.write(self._output_filename)
        self._document.close()

PluginClass = MailMergeTask
