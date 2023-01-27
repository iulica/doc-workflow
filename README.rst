
=================
Document Workflow
=================

.. image:: https://badge.fury.io/py/doc-workflow.png
    :alt: PyPI
    :target: https://pypi.python.org/pypi/doc-workflow

Creates, merges, splits, edits documents(mainly docx/pdf) as well as sending them by email.
Originally created for QR bills integration but is generic and can be used for much more.


Installation
============

Installation with ``pip``:
::

    $ pip install doc-workflow


Usage
=====

From the command line:
::

    $ docwf <path_to_json_config_file>

From Python:
::

    from docwf import DocWorkflow

    config_obj = {
        "globals": {
            "workbook": "source.xlsx",
            "sheet": "mailmergesheet",
            "constants": {
                "language": "fr"
            }
        },
        "tasks": [
            {
                "active": 1, # you can activate/deactivate tasks
                "name": "create bills", # name for debug purpose
                "locals": {
                    "key" : "value", # overrides global arguments for the task
                },
                "task": {
                    "type": "myplugin", # or builtin plugins (see below)
                    "task_dependent_argument": "value{param}",
                }
            },
        ]
    }
    my_plugins = {
        "myplugin": MyPluginClass
    }
    DocWorkflow(config_obj, plugins=my_plugins).gen()

Typical workflow tasks
======================

Assume the data is in the source.xlsx in the sheet named bills

========  ============  ==========  ======  =========  ======
clientnr  email         send_email  total   reference  etc 
========  ============  ==========  ======  =========  ======
1         c1@gmail.com     yes       1032   ref2022c1    ...
2         c2@gmail.com     yes       1232   ref2022c2    ...
========  ============  ==========  ======  =========  ======


Create bills from Word template
-------------------------------
::

    {
        "active": 1, # you can activate/deactivate tasks
        "name": "create bills", # name for debug purpose
        "task": {
            "type": "mailmerge",
            "input_docx": "templates/template_bill.docx",
            "output_docx": "bills/bill_{year}.docx" # output depends on the column year, it should be constant throughout all rows
        }
    },

Create pdf from the generated docx
-----------------------------------

It uses the Word Application (Mac/Windows).
If the docx template has dynamic fields (IF, etc), 
the generated docx will ask permission to update 
all fields before saving it as pdf.
::

    {
        "name": "save pdf from docx (uses Word)",
        "task": {
            "type": "makepdf",
            "input_docx": "bills/bill_{year}.docx",
            "output_pdf": "bills/bill_{year}.pdf"
        }
    },


Fills in QR codes
-------------------------------

for the bills by adding a page to each bill or by merging the QR bill into one of the pages.
::

    {
        "name": "create qr bills",
        "locals": {
            "creditor": {
                "iban": "CH....",
                "name": "The Good Company",
                "pcode": "xyzt",
                "city": "Bern",
                "street": "Dorfstrasse 1"
            },
            "task_params": {
                "extra_infos": "reference", # fixed keys for bill reason ...
                "amount": "total"   # and the amount. With task_params you can create data entries out of existing columns
            }
        },
        "task": {
            "type": "qr",
            "merge_type": "merge", # or "append"
            "input_filename": "bills/bill_{year}.pdf",
            "delete_input": true, # delete the input filename after creating the output
            "pages": 2, # the number of pages per each bill
            "merge_pos": 2, # or "insert_pos" if "append"
            "output_filename": "bills/bill_{year}_with_qr.pdf"
        }
    },

Split the bills into separate pdf files.
------------------------------------------

From one input to multiple outputs
::

    {
        "name": "split bills",
        "task": {
            "type": "split_pdf",
            "input_filename": "bills/bill_{year}_with_qr.pdf",
            "pages": 2,
            "makedir": "bills/bills_{year}", # if the output directory doesn't exist, create it
            "output_filename": "bills/bills_{year}/bill_{year}_{clientnr}.pdf" # output filename using unique name for each customer
        }
    },

Unify bills that are to be printed
------------------------------------------

This shows how to filter rows. The same split_pdf plugin is used, from multiple inputs to one output.
::

    {
        "name": "unify bills for print",
        "filter": {"column": "send_email", "value": "no"},
        "task": {
            "type": "split_pdf",
            "input_filename": "bills/bills_{year}/bill_{year}_{clientnr}.pdf",
            "delete_input": true,
            "pages": 2,
            "output_filename": "bills/bills_{year}_paper.pdf"
        }
    },

Send the bills by email
------------------------------------------

::

    {
        "name": "send emails",
        "locals": {
            "sender": {
                "email": "info@domain.com",
                "name": "Info",
                "server": "smtp.gmail.com:587",
                "username": "info@domain.com",
                "password": "strongpassword",
                "bcc": "bills@domain.com",
                "headers": {
                    "Reply-To": "contability@domain.com"
                }
            },
        },
        "filter": {"column": "send_email", "value": "yes"},
        "task": {
            "type": "email",
            "recipient": "email", # the key/column name for the customer email
            "subject" : "Bill for year {year}", # can contain dynamic parts
            "body_template_file" : "templates/email_template.txt", # text template for the email body
            "attachments" : [ "bills/bills_{year}/bill_{year}_{clientnr}.pdf" ] # list of attachments
        }
    },


Watermark PDF files
------------------------------------------

Mark reminder bills
::

    {
        "name": "save reminder",
        "filter": {"column": "reminder", "value": "yes"},
        "task": {
            "type": "watermark",
            "makedir": "bills/bills_{key_year}/reminders/",
            "watermark": "REMINDER",
            "input_filename": "bills/bills_{year}/bill_{year}_{clientnr}.pdf",
            "pages": 2,
            "output_filename": "bills/bills_{year}/reminders/bill_{year}_{clientnr}_reminder.pdf"
        }
    },

Send reminder bills
::

    {
        "name": "send reminder emails",
        "locals": {
            "sender": {
                ...
            },
        },
        "filter": [
            {"column": "send_email", "value": "yes"},
            {"column": "reminder", "value": "yes"}
        ],
        "task": {
            "type": "email",
            "recipient": "email", # the key/column name for the customer email
            "subject" : "Bill for year {year} (reminder)", # can contain dynamic parts
            "body_template_file" : "templates/reminder_email_template.txt", # text template for the email body
            "attachments" : [ "bills/bills_{year}/reminders/bill_{year}_{clientnr}_reminder.pdf" ] # list of attachments
        }
    },

Todo / Wish List
================

* Create unit tests
* Develop the command line to be able to run simple tasks directly
* Add Google Sheets support for the data
* Create more advanced filters
* Auto-magically create directories (remove the makedir argument)

Contributing
============

* Fork the repository on GitHub and start hacking
* Send a pull request with your changes


Credits
=======

This repository is created and maintained by `Iulian Ciorăscu`_.

.. _Iulian Ciorăscu: https://github.com/iulica/
