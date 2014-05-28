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
from datetime import datetime
import json

from delorean import parse
from bbhack.base import BasePublisher


class StreamDrillStreamer(BasePublisher):

    def __init__(self, zmq_string):
        BasePublisher.__init__(self, zmq_string, 'tweet.stream')

    def start(self, filename):
        with open(filename) as f:
            for line in f:
                parsed = json.loads(line)
                parsed_date = parse(parsed['created_at'])

                if self._should_post(parsed_date):
                    self.publish(line)

    def _should_post(self, parsed_date):
        n = datetime.now()
        d = parsed_date.datetime
        return (n.hour == d.hour and
                n.minute == d.minute and
                n.second == d.second)


def main():
    """Start the Streamdrill streamer"""

    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--filename')
    p.add_argument('--zmq_pub_string', default='tcp://*:5556')

    options = p.parse_args()

    stream = StreamDrillStreamer(options.filename,
                                 options.zmq_pub_string)

    # start streaming some stuff
    stream.start(options.filename)
