# Python SDK for Searpent Classy API

Simplify your calls to Searpent Classy API in Python.

## Installation

You can install the Searpent Python SDK from PyPI:

`pip install searpent-classy-sdk`

The SDK is supported on Python 3.6 to 3.10.

## How to use

1. Before you begin, make sure you have the API token and you know the name of your organization in the Classy API, e.g. 'dev.cz'.

2. Store your API_URL and API_TOKEN in local environment variables and run:

```
from classy_sdk import ClassySDK

client = ClassySDK('dev.cz')
```

or pass them as arguments to the class:

```
client = ClassySDK(source='dev.cz', api_url='some_url', api_token='your_token')
```

you can also specify a timeout (in seconds):

```
client = ClassySDK(source='dev.cz', timeout=10)
```

3. Use your `client` to make API calls. For instance:

```
client.list_cases(from_time='2021-09-01T13:00:00.000Z',
                  to_time='2021-10-02T13:00:00.000Z')
client.get_case('ce4c0299-6518-441b-b43d-1eeae666db36')
new_name = client.create_case('test_case')
client.update_case(new_name, 'test_case_updated')
client.upload_photo_from_file(new_name, 'tests/data/test_image.jpg',
                              'test_image', 'test_image')
```

4. These are the methods that are currently available: 

* list_cases:
    Retrieves a list of cases within an indicated time period.
* get_case:
    Retrieves one particular case.
* get_case_with_photos:
    Retrieves one particular case with photos.
* create_case:
    Creates a new case.
* update_case:
    Updates the case name as displayed in the Classy interface.
* delete_case:
    Marks the case to be deleted after 3 days.
* cancel_delete_case:
    Cancels the case deletion.
* postpone_delete_case:
    Postpones the case deletion to a requested timepoint.
* upload_photo:
    Uploads a photo in base64 format to the case.
* upload_photo_from_file:
    Uploads a photo file to the case.
* upload_pdf:
    Uploads a PDF in base64 format to the case.
* upload_pdf_from_file:
    Uploads a PDF file to the case.
* list_exports:
    Retrieves a list of performed exports.
* get_export:
    Retrieves one particular export.
* get_export_csv:
    Retrieves a csv file with requested export.
* get_export_download_url:
    Retrieves a csv download url for the requested export.
* list_inspections:
    Retrieves a list of performed inspections.
* get_inspection:
    Retrieves one particular inspection.
* get_inspection_with_photos:
    Retrieves one particular inspection with photos.
* create_inspection:
    Creates a new inspection.
* delete_inspection:
    Marks the inspection to be deleted after 3 days.
* cancel_delete_inspection:
    Cancels the inspection deletion.
* postpone_delete_inspection:
    Postpones the inspection deletion to a requested timepoint.

## API documentation

See the complete API documentation: [searpentclassy.docs.apiary.io](https://searpentclassy.docs.apiary.io).