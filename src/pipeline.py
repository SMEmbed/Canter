#!/usr/bin/env python
import sys

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst, GLib

import properties


class Pipeline():
    def __init__(self, pipeline_str, json_file):
        Gst.init(None)
        pipeline = Gst.parse_launch(pipeline_str)

        self.loop = GLib.MainLoop()

        self.schema_file = 'pipeline_schema.json'
        properties.dump_to_json_schema(pipeline, self.schema_file)
        properties.load_from_json(pipeline, json_file, self.schema_file)

        self.pipeline = pipeline
        bus = pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.bus_call, self.loop)

    def play(self):
        self.pipeline.set_state(Gst.State.PLAYING)
        self.loop.run()
        
    def bus_call(self, bus, message, loop):
        t = message.type
        if t == Gst.MessageType.EOS:
            sys.stdout.write("End-of-stream\n")
            loop.quit()
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            sys.stderr.write("Error: %s: %s\n" % (err, debug))
            loop.quit()
        #print('message type is {}'.format(t))
        return True
