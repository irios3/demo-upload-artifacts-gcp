#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import argparse
import asyncio
import logging
import os
import sys

from aiohttp_retry import RetryClient


log = logging.getLogger(__name__)

BITRISE_APP_SLUG_ID = "027987c04521af20"
BITRISE_URL_TEMPLATE = "https://api.bitrise.io/v0.1/apps/" + BITRISE_APP_SLUG_ID + "/{suffix}"


class TaskException(Exception):
    def __init__(self, *args, exit_code=1):
        """Initialize ScriptWorkerTaskException.
        Args:
            *args: These are passed on via super().
            exit_code (int, optional): The exit_code we should exit with when
                this exception is raised.  Defaults to 1 (failure).
        """
        self.exit_code = exit_code
        super(Exception, self).__init__(*args)


async def download_log(client, build_slug, artifacts_directory):
    suffix = "builds/{}/log".format(build_slug)
    url = BITRISE_URL_TEMPLATE.format(suffix=suffix)

    while True:
        response = await do_http_request_json(client, url)
        if response["is_archived"] == True:
            log.info("Log is now ready")
            break
        else:
            log.info("Log is still running. Waiting another minute...")
            await asyncio.sleep(60)

    download_url = response["expiring_raw_log_url"]
    if download_url:
        await download_file(download_url, os.path.join(artifacts_directory, "bitrise.log"))
    else:
        log.error("Bitrise has no log to offer for job {0}. Please check https://app.bitrise.io/build/{0}".format(build_slug))



CHUNK_SIZE = 128


async def download_file(download_url, file_destination):
    async with RetryClient() as s3_client:
        async with s3_client.get(download_url) as resp:
            with open(file_destination, "wb") as fd:
                while True:
                    chunk = await resp.content.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    fd.write(chunk)

    log.info("'{}' downloaded".format(file_destination))


async def do_http_request_json(client, url, method="get", **kwargs):
    method_and_url = "{} {}".format(method.upper(), url)
    log.debug("Making request {}...".format(method_and_url))

    http_function = getattr(client, method)
    async with http_function(url, **kwargs) as r:
        log.debug("{} returned HTTP code {}".format(method_and_url, r.status))
        response = await r.json()

    log.debug("{} returned JSON {}".format(method_and_url, response))

    return response



