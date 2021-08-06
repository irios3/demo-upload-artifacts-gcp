#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import argparse
import asyncio
import logging
import os
import sys
import requests



BITRISE_APP_SLUG_ID = "027987c04521af20"
BITRISE_URL_TEMPLATE = "https://api.bitrise.io/v0.1/apps/" + BITRISE_APP_SLUG_ID + "/{suffix}"


def download_log(build_slug):
    suffix = "builds/{}/log".format(build_slug)
    url = BITRISE_URL_TEMPLATE.format(suffix=suffix)

    while True:
        response = do_http_request_json(url)
        if response["is_archived"] == True:
            print("Log is ready")
            log.info("Log is now ready")
            break
        else:
            print("Log not ready")
            log.info("Log is still running. Waiting another minute...")
            asyncio.sleep(60)

    download_url = response["expiring_raw_log_url"]
    if download_url:
        print("download url")
    else:
        log.error("Bitrise has no log to offer for job {0}. Please check https://app.bitrise.io/build/{0}".format(build_slug))



def do_http_request_json(url):
    #method_and_url = "{} {}".format(method.upper(), url)
    #log.debug("Making request {}...".format(method_and_url))
    print("making reguest")
    print(url)
    
    data = requests.get(url)
    response = data.json()
    #log.debug("{} returned JSON {}".format(method_and_url, response))
    print(response)

    return response


download_log(BITRISE_APP_SLUG_ID)
