import json

import mock
from kivy.base import EventLoopBase


class TestUtils():

    def __init__(self):
        self.mock_patches = [
           mock.patch('kivy.uix.widget.Builder'),
           mock.patch.object(EventLoopBase, 'ensure_window', lambda x: None),
         ]

    def load_json_from_file(self, filename):
        with open(filename) as f:
            data = json.load(f)
        return data

    def start_kivy_windowing_stub(self):
        for patch in self.mock_patches:
            patch.start()

    def stop_kivy_windowing_stub(self):
        for patch in self.mock_patches:
            patch.stop()