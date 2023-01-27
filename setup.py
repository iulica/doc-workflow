
from distutils.core import setup
setup(
  name='doc-workflow',
  packages=['docwf', 'docwf.plugins'],
  version='0.1.0-alpha10',
  license='MIT',
  description='A Python Document Management Framework for generating and sending (pdf, docx, etc) documents to customers',
  long_description=open('README.rst', encoding="utf-8").read(),
  # long_description_content_type='text/x-rst',
  author='Iulian Ciorăscu',
  author_email='ciulian@gmail.com',
  url='https://github.com/iulica/doc-workflow',
  entry_points={
    'console_scripts': [
        'docwf = docwf.docwf:DocWorkflow.cli',
    ],
  },
  keywords=['docx', 'pdf', 'split', 'watermark', 'email', 'mailmerge', 'qrbill', 'xlsx'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Customer Service',
    'Intended Audience :: Information Technology',
    'Topic :: Office/Business :: Financial :: Accounting',
    'Topic :: Utilities',
    'Topic :: Text Processing',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
  install_requires = [
    "PyPDF2",
    "cairosvg",
    "qrbill",
    "openpyxl",
    "svglib",
    "reportlab",
    "docx-mailmerge2",
    "docx2pdf"
  ]
)
