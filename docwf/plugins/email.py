""" email plugin - sends emails with bills """


from os.path import basename
from email.message import EmailMessage

import ssl
import smtplib
import glob


from .base import BasePlugin

class Email3Task(BasePlugin):

    """ class used for the send emails task """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._sender = self._globals_dict['sender']
        self._smtp = None

    def _connect_to_smtp(self):
        if self._smtp is None:
            server_name, server_port = self._sender['server'].split(':')
            context = ssl.create_default_context()
            smtp = smtplib.SMTP(server_name, server_port)
            smtp.ehlo() # Can be omitted
            smtp.starttls(context=context) # Secure the connection
            smtp.ehlo() # Can be omitted
            smtp.login(self._sender['username'], self._sender['password'])
            self._smtp = smtp
        return self._smtp

    def _send_email(self, value_dict):
        smtp = self._connect_to_smtp()
        recipient = value_dict[self._task_info['recipient']]
        if not recipient:
            print("ignored, no email")
            return
        with open(self._task_info['body_template_file'], "r", encoding="utf-8") as template_file:
            message = template_file.read()
        message = message.format(**value_dict)
        subject = self._task_info['subject'].format(**value_dict)
        attachments = [
            attachment.format(**value_dict)
            for attachment in self._task_info.get('attachments', [])
        ]

        msg = EmailMessage()
        msg['From'] = self._sender['username']
        msg['To'] = recipient
        # msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
        bcc = self._sender.get('bcc')
        if bcc:
            msg['Bcc'] = bcc
        if 'headers' in self._sender:
            for key, value in self._sender['headers'].items():
                msg[key] = value.format(**value_dict)

        msg.set_content(message)
        for attachment in attachments:
            for filename in glob.glob(attachment):
                with open(filename, 'rb') as pdf_file:
                    msg.add_attachment(
                        pdf_file.read(),
                        maintype='application',
                        subtype='pdf',
                        filename=basename(filename))
        
        # print(msg)
        smtp.send_message(msg)

    def do_task(self, value_dict, **kwargs):
        return self._send_email(value_dict)

    def finish(self):
        if self._smtp is not None:
            self._smtp.quit()

PluginClass = Email3Task