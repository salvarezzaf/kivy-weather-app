import json

import mock
from kivy.base import EventLoopBase
from kivy.uix.textinput import TextInput


class TestUtils:

    def __init__(self):
        pass

    mock_patches = [
       mock.patch('kivy.uix.widget.Builder'),
       mock.patch.object(EventLoopBase, 'ensure_window', lambda x: None)
    ]

    @staticmethod
    def load_json_from_file(filename):
        with open(filename) as f:
            data = json.load(f)
        return data

    @staticmethod
    def start_kivy_windowing_stub():
        for patch in TestUtils.mock_patches:
            patch.start()

    @staticmethod
    def stop_kivy_windowing_stub():
        for patch in TestUtils.mock_patches:
            patch.stop()