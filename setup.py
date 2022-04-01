
from distutils.core import setup
setup(
  name = 'doc-workflow',         # How you named your package folder (MyLib)
  packages = ['docwf'],   # Chose the same as "name"
  version = '0.1.0-alpha',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A Python Document Management Framework for generating and sending (pdf, docx, etc) documents to customers',   # Give a short description about your library
  author = 'Iulian Ciorăscu',                   # Type in your name
  author_email = 'ciulian@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/iulica/doc-workflow',   # Provide either the link to your github or to your website
  entry_points={
    'console_scripts': [
        'docwf = docwf.docwf:DocWorkflow.cli',
    ],
  },
  # download_url = 'https://github.com/iulica/doc-workflow/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['docx', 'pdf', 'split', 'watermark', 'email', 'mailmerge', 'qrbill', 'xlsx'],   # Keywords that define your package best
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Customer Service',
    'Intended Audience :: Information Technology',
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Office/Business :: Financial :: Accounting',
    'Topic :: Utilities',
    'Topic :: Text Processing',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)