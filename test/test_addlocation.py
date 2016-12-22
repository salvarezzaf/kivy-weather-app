import unittest

from kivy.uix.textinput import TextInput
from mock import mock, Mock
from mock.mock import MagicMock

from app.addlocation import AddLocation
from test.testutils import TestUtils


class TestAddLocation(unittest.TestCase):

    def setUp(self):
        TestUtils.start_kivy_windowing_stub()
        self.data = TestUtils.load_json_from_file("test/add_city_autocomplete.json")
        self.add_location = AddLocation()

    @mock.patch('kivy.uix.textinput.TextInput')
    @mock.patch('app.addlocation.UrlRequest')
    @mock.patch('kivy.properties.ObjectProperty')
    def test_search_query_city(self, mock_input, mock_request, mock_results):
        mock_input = MagicMock(text="Glasgow")
        self.add_location.search_input = mock_input
        mock_results = MagicMock()
        self.add_location.results = mock_results
        mock_request = Mock()
        mock_request.side_effect = self.add_location.display_results(mock_request.request, self.data)
        self.add_location.search_query_city()
        self.assertTrue(len(self.add_location.results.item_strings) == 1)
        self.assertEqual(self.add_location.results.item_strings[0], "Glasgow, United Kingdom")

    @mock.patch('kivy.uix.textinput.TextInput')
    @mock.patch('kivy.properties.ObjectProperty')
    def test_search_query_city_returns_empty_results(self, mock_input, mock_results):
        mock_input = MagicMock(text="G")
        self.add_location.search_input = mock_input
        mock_results = MagicMock()
        self.add_location.results = mock_results
        self.add_location.search_query_city()
        self.assertTrue(self.add_location.results.item_strings[0] == '')

    def tearDown(self):
        TestUtils.stop_kivy_windowing_stub()