""" split plugin - split collection pdf into smaller pdfs """

from .base import BasePlugin

class SplitPdfTask(BasePlugin):

    """ class used for the split pdf task """

    def do_task(self, value_dict, **kwargs):
        input_stream, output_stream = self._task_helper.get_io_streams(value_dict)
        page_start = self._task_info.get('split_start_page', 0)
        page_end = page_start + self._task_info.get('split_pages', self._task_helper.pages_per_bill)
        for page in list(input_stream.readPages(self._task_helper.pages_per_bill))[page_start:page_end]:
            output_stream.add_page(page)

PluginClass = SplitPdfTask
