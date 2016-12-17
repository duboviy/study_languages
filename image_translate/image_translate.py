#!/usr/bin/env python

"""
This script uses the Google Cloud Vision Python API's label detection capabilities to find a translation
based on an image's content.

To run the example, install the necessary libraries by running:

    pip install -r requirements.txt

Run the script on an image to get a translation, E.g.:

    ./label.py <path-to-image>
"""

import argparse
import base64
import logging as log

# you need to install google api engine sdk
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

import translate


def _authenticate():
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials)
    return service


def _construct_request(photo_file, service):
    with open(photo_file, 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'LABEL_DETECTION',
                    'maxResults': 1
                }]
            }]
        })
    return service_request


def _send_request(service_request):
    response = service_request.execute()
    return response


def _parse_response(response):
    label = response['responses'][0]['labelAnnotations'][0]['description']
    return label


def _get_image_content_label(photo_file):
    """Run a label request on a single image"""
    log.basicConfig(level=log.INFO, format='%(message)s')

    service = _authenticate()
    service_request = _construct_request(photo_file, service)
    response = _send_request(service_request)
    label = _parse_response(response)

    log.info('Found label: %s for %s' % (label, photo_file))

    return label


def image_translate(photo_file, output_lang, source_lang='en'):
    label = _get_image_content_label(photo_file)
    translated_result = translate.translator(source_lang, output_lang, label)

    log.info('Translated result for label: %s is %s' % (label, translated_result))

    return translated_result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file', help='The image you\'d like to label.')
    parser.add_argument('output_lang', help='Output translation language.')
    args = parser.parse_args()

    translated_result = image_translate(args.image_file, args.output_lang)
    return translated_result


if __name__ == "__main__":
    # run with params, for example:
    # >>> python image_translate.py resources/cat.jpg fr
    main()
