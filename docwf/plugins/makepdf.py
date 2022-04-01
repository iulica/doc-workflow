""" mailmerge plugin - mailmerge a docx """

from .base import BasePlugin
import docx2pdf

class MailMergeTask(BasePlugin):

    """ class used for the docx mailmerge task """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._input_filename = None
        self._output_filename = None

    def _init_filenames(self, value_dict):
        self._input_filename = self._task_info['input_docx'].format(**value_dict)
        self._output_filename = self._task_info['output_pdf'].format(**value_dict)
        
    def do_task(self, value_dict, **kwargs):
        if self._input_filename is None:
            self._init_filenames(value_dict)
    
    def finish(self):
        docx2pdf.convert(
            self._input_filename, self._output_filename,
            keep_active=self._task_info.get("keep_active", False))

PluginClass = MailMergeTask
