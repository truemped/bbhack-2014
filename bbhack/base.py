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

from abc import ABCMeta, abstractmethod
import json

import traceback
import zmq


class BaseListener(object):
    """Base class for subscribing tweets from an upstream ZMQ socket."""

    __metaclass__ = ABCMeta

    def __init__(self, zmq_sub_string, channel):
        self._ctx = zmq.Context.instance()
        self._subscriber = self._ctx.socket(zmq.SUB)
        self._subscriber.connect(zmq_sub_string)
        self._subscriber.setsockopt(zmq.SUBSCRIBE, channel)

    def start(self):
        """Start listening for new tweets."""
        while True:
            (_, tweet_json) = self._subscriber.recv_multipart()
            try:
                self.on_msg(json.loads(tweet_json))
            except Exception:
                traceback.print_exc()
                raise

    @abstractmethod
    def on_msg(self, msg):
        """Called when a new tweet arrives. The tweet is json parsed and is
        represented as a simple Python dict."""


class BasePublisher(object):
    """Base class for publishing messages."""

    def __init__(self, zmq_pub_string, channel):
        self._ctx = zmq.Context.instance()
        self._publisher = self._ctx.socket(zmq.PUB)
        self._publisher.bind(zmq_pub_string)
        self._channel = channel

    def publish(self, msg):
        self._publisher.send_multipart([self._channel, msg])
