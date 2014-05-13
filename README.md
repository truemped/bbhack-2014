Getting started
===============


Preparing your environment

$ python bootstrap.py
$ bin/buildout

This will download all necessary dependencies (twython, pyzmq) and compile
them.


Contents
--------

The `bbhack.base.BaseListener` class can be used to subscribe to messages from a
ZeroMQ socket and a channel. The `bbhack.base.BasePublisher` can be used for
publishing messages to a ZeroMQ socket and channel.

The `bbhack.streamer.TweetStreamer` is an example for the `BasePublisher`. It
simply connects to the twitter streaming api tracking for keywords and publishes
the tweets on the given ZeroMQ socket and the `tweet.stream` channel.

An example for the `BaseListener` is given in `bbhack.example.HashTagLogger`.
This listener will connect to a socket and subscibe to a given channel and then
simply log all hashtags that are found in tweets.

Both modules contain a `main()` method that is used for the `entry_point`
declaration in the `setup.py`.
