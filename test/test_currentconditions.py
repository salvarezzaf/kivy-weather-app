import unittest
import urllib

from kivy.network.urlrequest import UrlRequest
from mock import patch, MagicMock
import mock

from app.currentconditions import CurrentCondition
from app.dbutil import DbUtil
from app.models.models import Location
from app.weatherutil import WeatherUtil
from test.testutils import TestUtils


class TestCurrentConditions(unittest.TestCase):

    def setUp(self):
        self.current_conditions = CurrentCondition()
        self.test_utils = TestUtils()
        self.data = self.test_utils.load_json_from_file("test/glasgow_conditions_response.json")
        self.forecast = self.test_utils.load_json_from_file("test/forecast.json")
        self.degree_symbol = u"\u00B0"
        self.current_temp = '3'+ self.degree_symbol
        self.highlow_temps = '11' + self.degree_symbol + '/' + '6' + self.degree_symbol

    @patch.object(DbUtil, 'get_default', MagicMock(return_value=Location(location_name="Glasgow",
                                                                                 location_code="UK",
                                                                                 location_lat="12.334",
                                                                                 location_long="55,345",
                                                                                 isDefault=True)))
    @patch.object(DbUtil,'get_default_tem_unit', MagicMock(return_value="celsius"))
    @patch.object(WeatherUtil, 'get_icon_for_conditions', MagicMock(return_value="app/img/clear.png"))
    @mock.patch('app.currentconditions.UrlRequest')
    def test_get_current_conditions(self,mock_url_request):
        mock_url_request = MagicMock()
        mock_url_request.side_effect = [self.current_conditions.parse_current_weather_data(mock_url_request.request,self.data),
                                        self.current_conditions.parse_high_low_temperature(mock_url_request.request,self.forecast)]
        self.current_conditions.get_current_conditions()
        self.assertEqual(str(self.current_conditions.current_location_name), "Glasgow,UK")
        self.assertEqual(str(self.current_conditions.current_condition_text), "Clear")
        self.assertEqual(str(self.current_conditions.current_condition_img), "app/img/clear.png")
        self.assertEqual(self.current_conditions.current_temp, self.current_temp)
        self.assertEqual(self.current_conditions.high_low_temps, self.highlow_temps)





