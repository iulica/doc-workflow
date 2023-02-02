""" mailmerge plugin - mailmerge a docx """

from io import BytesIO
import gspread, gspread.urls, gspread.utils
from PyPDF2 import PdfReader
from .base import BasePlugin
from .data_gspread import GspreadWorkbook


class PrintSheetsTask(BasePlugin):

    """ class used for printing spreadsheets as pdf task """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert 'sheet' in kwargs and 'workbook' in kwargs
        assert isinstance(kwargs['workbook'], GspreadWorkbook)

        self._workbook = kwargs['workbook']

        self._output_stream = None

    # def _init_filenames(self, value_dict):
    #     self._output_filename = self._task_info['output_pdf'].format(**value_dict)
        
    def do_task(self, value_dict, **kwargs):
        if self._output_stream is None:
            _, self._output_stream = self._task_helper.get_io_streams(value_dict)
    
    def finish(self):
        gc = gspread.service_account_from_dict(self._globals_dict['data']['credentials'])
        printsheet_defaults = self._globals_dict.get('printsheets_defaults', {})
        for sheet_info in self._task_info['printsheets']:
            params = {}
            params["format"] = "pdf"
            params.update(printsheet_defaults)
            params.update(sheet_info)
            url = "{}/export".format(gspread.urls.SPREADSHEET_DRIVE_URL % self._workbook._workbook.id)
            # print(params, url)
            # print(gc.export(self._workbook._workbook.id))
            r = gc.request("get", url, params=params)

            pdf_out = BytesIO()
            pdf_out.write(r.content)
            pdf_out.seek(0)
            sheet_pdf = PdfReader(pdf_out)
            # # with open(self._output_filename, "wb") as out_pdf:
            # #     out_pdf.write(r.content)
            self._output_stream.append_pages_from_reader(sheet_pdf)

            # for page in sheet_pdf.readPages():
            #     output_stream.add_page(page)



PluginClass = PrintSheetsTask
