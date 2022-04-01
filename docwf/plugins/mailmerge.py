""" mailmerge plugin - mailmerge a docx """

from .base import BasePlugin
from mailmerge import MailMerge

class MailMergeTask(BasePlugin):

    """ class used for the docx mailmerge task """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert 'sheet' in kwargs
        self._column_map = {
            cell.value.strip().lower().replace(' ', '_'): cell.column - 1
            for cell in kwargs['sheet'][1]
            if cell.value
        }
        self._rows = []
        self._document = None
        self._fields = None
        self._output_filename = None

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
            field_name: row[self._column_map[field_name.lower()]].value
            for field_name in self._fields
        }

        self._rows.append(data_dict)
    
    def finish(self):

        # print(merge_data)
        separator = self._task_info.get('separator', 'page_break')
        self._document.merge_templates(self._rows, separator=separator)
        self._document.write(self._output_filename)
        self._document.close()

PluginClass = MailMergeTask
