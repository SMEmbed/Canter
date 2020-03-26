#!/usr/bin/env python

import sys

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst, GLib

import properties

def bus_call(bus, message, loop):
    t = message.type
    if t == Gst.MessageType.EOS:
        sys.stdout.write("End-of-stream\n")
        loop.quit()
    elif t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        sys.stderr.write("Error: %s: %s\n" % (err, debug))
        loop.quit()
    print('message type is {}'.format(t))
    return True

Gst.init(None)
pipeline = Gst.parse_launch('videotestsrc ! x264enc ! autovideosink')

loop = GLib.MainLoop()
bus = pipeline.get_bus()
bus.add_signal_watch()
bus.connect ("message", bus_call, loop)

element = pipeline.children[1]
#element.props.num_buffers = 20
properties.dump_to_json_schema(pipeline)
properties.load_from_json(pipeline)
pipeline.set_state(Gst.State.PLAYING)

#loop.run()
#When the process finishes, the pipeline stops
import time
time.sleep(1)
