# vim: set fileencoding=utf-8 :
#
# Copyright (c) 2013 Daniel Truemper <truemped at googlemail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
from __future__ import (absolute_import, division, print_function,
                        with_statement)

import json
import logging

from twython import TwythonStreamer

from bbhack.base import BasePublisher


LOG = logging.getLogger(__name__)


class TweetStreamer(TwythonStreamer, BasePublisher):
    """Simple twitter streaming api client that publishes tweets to a ZeroMQ
    socket. The tweets are published in the channel `tweet.stream`."""

    def __init__(self, consumer_key, consumer_secret, access_token,
                 access_token_secret, zmq_pub_string):
        TwythonStreamer.__init__(self, consumer_key, consumer_secret,
                                 access_token, access_token_secret)
        BasePublisher.__init__(self, zmq_pub_string, 'tweet.stream')

    def on_error(self, status_code, tweet):
        LOG.error('Error in the streamer (code=%s, tweet=%s)' % (
            status_code, tweet))

    def on_success(self, tweet):
        """A new tweet has arrived"""
        try:
            self.publish(json.dumps(tweet))
        except Exception as e:
            LOG.exception('Error processing the tweet (id=%s)' % tweet['id'],
                          e)


def main():
    """Start the Twitter streamer"""

    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--consumer_key')
    p.add_argument('--consumer_secret')
    p.add_argument('--access_token')
    p.add_argument('--access_token_secret')
    p.add_argument('--zmq_pub_string', default='tcp://*:5556')
    p.add_argument('--track', default='twitter')

    options = p.parse_args()

    stream = TweetStreamer(options.consumer_key, options.consumer_secret,
                           options.access_token, options.access_token_secret,
                           options.zmq_pub_string)

    # start streaming some stuff
    stream.statuses.filter(track=options.track)
