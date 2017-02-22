# Copyright 2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not
# use this file except in compliance with the License. A copy of the License is
# located at
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

from __future__ import print_function
import logging
import requests
from bs4 import BeautifulSoup


print('Loading comidaBot function')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

URL = 'http://foodtruckfiesta.com/dc-food-truck-list/'
AVAILABLE_LOCATIONS = {
    'npr': {
        'areas': ['NoMa', 'CNN', 'Union Station'],
        'extra': 'Here\'s the SoundBites menu for this week: https://intranet.npr.org/intranet/publish/Main/Employee_Resources/Sound_Bites_Cafe.php'
    },
    'bid': {
        'areas': [],
        'extra': None
    }
}


def lambda_handler(event, context):
    logger.debug(event)
    bot_event = event
    raw_text = bot_event['text']
    location = raw_text.strip().lower()
    logger.debug("Raw Text: %s" % raw_text)
    result = ''
    if location in AVAILABLE_LOCATIONS:
        response = requests.get(URL)
        if (response.status_code != 200):
            logger.error("page responded with %s code" % response.status_code)
            result += 'Could not get food truck data.\n'
        else:
            areas = AVAILABLE_LOCATIONS[location]['areas']
            for area in areas:
                result += '\n## ' + area + '\n'
                # TODO parse food truck page
            extra = AVAILABLE_LOCATIONS[location]['extra']
            if extra:
                result += '\n\n%s\n\n' % extra
            # Check to see if our result is still empty and warn user
            if result == '':
                result += 'No available areas for your location'
    else:
        result += "Your location is not available. Available locations:\n"
        for key in AVAILABLE_LOCATIONS:
            result += '-%s\n' % key

    return {'text': result}
