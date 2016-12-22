import unittest
from mock import MagicMock, mock, Mock, patch

from app.dbutil import DbUtil
from app.locationforecast import LocationForecast
from app.models.models import Location
from test.testutils import TestUtils


class TestLocationForecast(unittest.TestCase):

    def setUp(self):
        TestUtils.start_kivy_windowing_stub()
        self.forecast = LocationForecast()
        self.data = TestUtils.load_json_from_file("test/forecast.json")

    @patch.object(DbUtil, 'get_default', MagicMock(
        return_value=Location(location_name="Glasgow", location_code="UK", location_lat="12.334",
                              location_long="55,345", isDefault=True)))
    def test_get_weather_forecast(self):
        self.forecast.get_weather_forecast()

    def tearDown(self):
        TestUtils.stop_kivy_windowing_stub()