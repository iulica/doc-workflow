""" qr plugin - adds qr to bills """

from io import BytesIO, StringIO
import tempfile
from PyPDF2 import PdfReader

from qrbill.bill import QRBill
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

from .base import BasePlugin

DEBTOR_KEYS = [
    "debtor_name", "debtor_city", "debtor_street", "debtor_pcode"
]

class QRBillMaker():

    def __init__(self, creditor, iban_nr=None):
        if iban_nr is None:
            self.iban_nr = creditor['iban']
        else:
            self.iban_nr = iban_nr

        self.creditor = {
            key: value
            for key, value in creditor.items()
            if key != "iban"
        }
    
    def create_bill(self, value_dict):
        debtor = {
            key: value_dict[key]
            for key in DEBTOR_KEYS
            if key in value_dict
        }
        if not debtor:
            debtor = None
        amount = value_dict['amount']
        if not amount or float(amount) <= 0:
            return None
        amount = str(round(float(amount), 2))

        try:
            my_bill = QRBill(
                account=self.iban_nr,
                creditor=self.creditor,
                amount=amount,
                debtor=debtor,
                extra_infos=value_dict['extra_infos'],
                language=value_dict.get('language', 'de')
            )
        except:
            print(value_dict)
            raise

        # generate the qr bill as pdf in pdf_out
        # svg_out = BytesIO(encoding="utf-8")
        pdf_out = BytesIO()
        # TODO use StringIO() for svg generation
        with tempfile.TemporaryFile(mode='r+', encoding='utf-8') as svg_out:
            my_bill.as_svg(svg_out, full_page=True)
            svg_out.seek(0)
            drawing = svg2rlg(svg_out)

        # svg_filename = 'bills/svg/temp.svg'.format(
        #     **value_dict)
        # pdf_filename = 'bills/{}_{}.pdf'.format(jahrgang, hausnr)
        # print(drawing)
        pdf_out.write(renderPDF.drawToString(drawing))
        pdf_out.seek(0)
        return pdf_out


class QRTask(BasePlugin):

    """ class used for the qr bill generation task """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.qr_bill_maker = QRBillMaker(self._globals_dict['creditor'])
        self._merge_type = self._task_info.get('merge_type', 'append')

    def _merge_bill_page(self, pages, qrbill_page):
        # TODO add this as a merge task mixin
        if self._merge_type == 'append':
            insert_pos = self._task_info.get('insert_pos', self._task_helper.pages_per_bill + 1) - 1
            pages.insert(insert_pos, qrbill_page)
            return
        
        if self._merge_type == 'merge':
            merge_pos = self._task_info.get('merge_pos', 1) - 1
            qrbill_page.merge_page(pages[merge_pos])
            pages[merge_pos] = qrbill_page
            return
        
        raise RuntimeError('Invalid merge type {}'.format(self._merge_type))

    def do_task(self, value_dict, **kwargs):
        input_stream, output_stream = self._task_helper.get_io_streams(value_dict)
        pages = list(input_stream.readPages(self._task_helper.pages_per_bill))
        bill_pdf = self.qr_bill_maker.create_bill(value_dict)
        if bill_pdf:
            qrbill_page = PdfReader(bill_pdf).pages[0]
            self._merge_bill_page(pages, qrbill_page)

        for page in pages:
            output_stream.add_page(page)
        
PluginClass = QRTask