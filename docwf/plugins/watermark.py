""" watermark plugin - watermark all pages of a document """

from PyPDF2 import PdfFileReader
from .pdf_watermark import create_watermark
from .base import BasePlugin

class WatermarkTask(BasePlugin):

    """ class used for the watermarking task """

    def _watermark(self, input_stream, output_stream, value_dict):
        # create watermark
        watermark_text = self._task_info['watermark']
        watermark_pdf_page = PdfFileReader(create_watermark(watermark_text)).getPage(0)
        for page in input_stream.readPages(self._task_helper.pages_per_bill):
            page.mergePage(watermark_pdf_page)
            output_stream.addPage(page)

    def do_task(self, value_dict, **kwargs):
        input_stream, output_stream = self._task_helper.get_io_streams(value_dict)
        return self._watermark(input_stream, output_stream, value_dict)

PluginClass = WatermarkTask
