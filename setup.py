# vim: set fileencoding=utf-8 :
#
# Copyright (c) 2012 Daniel Truemper <truemped at googlemail.com>
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

import sys

try:
    # Use setuptools if available, for install_requires (among other things).
    import setuptools
    from setuptools import setup
except ImportError:
    setuptools = None
    from distutils.core import setup

tests_require = [
    'pytest',
    'pytest-cov',
]

if sys.version_info < (2, 7):
    tests_require.append('unittest2')

extras_require = {}
extras_require['test'] = tests_require

setup(
    name='bbhack',
    version='0.1.0',

    author='Daniel Truemper',
    author_email='truemped@gmail.com',

    description='',
    packages=['bbhack'],

    install_requires=[
        'twython',
        'pyzmq',
        'delorean'
    ],

    tests_require=tests_require,
    extras_require=extras_require,

    entry_points={
        'console_scripts': [
            'streamer=bbhack.streamer:main',
            'hashtag-logger=bbhack.example:main',
        ]
    }
)
