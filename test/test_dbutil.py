import unittest

from mock import patch, Mock, MagicMock
from sqlalchemy.orm import Session
from app.dbutil import DbUtil
from app.models.models import Location, Settings, Base
from test.testutils import TestUtils


class TestDbUtil(unittest.TestCase):

    def setUp(self):
        self.in_memory_db_uri = "sqlite:///:memory:"
        self.test_location = {
            "location_name":"Napoli",
            "location_code":"IT",
            "location_lat":"12.123",
            "location_long": "55.123",
            "isDefault":True
        }
        self.test_location_obj = Location(location_name=self.test_location['location_name'],
                                 location_code=self.test_location['location_code'],
                                 location_lat=self.test_location['location_lat'],
                                 location_long=self.test_location['location_long'],
                                 isDefault=self.test_location['isDefault'])
        self.db_util = DbUtil()
        self.test_util = TestUtils()

    def test_create_db_session(self):
        test_session = DbUtil.create_db_session(self.in_memory_db_uri)
        engine = test_session.get_bind()
        self.assertIsInstance(test_session,Session)
        self.assertEqual(str(engine.url),self.in_memory_db_uri)
        test_session.close()

    @patch.object(DbUtil,'create_db_session', MagicMock(return_value=DbUtil.create_db_session("sqlite:///:memory:")))
    def test_obj_save (self):
        self.db_util.save(self.test_location_obj)
        self.assertTrue(self.db_util.location_exists(self.test_location['location_name']))

    @patch.object(DbUtil, 'create_db_session', MagicMock(return_value=DbUtil.create_db_session("sqlite:///:memory:")))
    def test_location_exists(self):
        self.assertFalse(self.db_util.location_exists(self.test_location['location_name']))
        self.db_util.save(self.test_location_obj)
        self.assertTrue(self.db_util.location_exists(self.test_location['location_name']))

    @patch.object(DbUtil, 'create_db_session', MagicMock(return_value=DbUtil.create_db_session("sqlite:///:memory:")))
    def test_remove_existing_default(self):
        self.db_util.save(self.test_location_obj)
        self.db_util.remove_existing_default()
        self.assertIsNone(self.db_util.get_default())

    @patch.object(DbUtil, 'create_db_session', MagicMock(return_value=DbUtil.create_db_session("sqlite:///:memory:")))
    def test_get_default(self):
        self.db_util.save(self.test_location_obj)
        self.assertIsNotNone(self.db_util.get_default())

    @patch.object(DbUtil, 'create_db_session', MagicMock(return_value=DbUtil.create_db_session("sqlite:///:memory:")))
    def test_find_all(self):
        self.db_util.save(self.test_location_obj)
        results = self.db_util.find_all()
        self.assertTrue(len(results)==1)

    @patch.object(DbUtil, 'create_db_session', MagicMock(return_value=DbUtil.create_db_session("sqlite:///:memory:")))
    def test_set_default(self):
        self.assertIsNone(self.db_util.get_default())
        self.test_location_obj.isDefault=False
        self.db_util.save(self.test_location_obj)
        self.db_util.set_default(self.test_location['location_name'])
        self.assertIsNotNone(self.db_util.get_default())

    @patch.object(DbUtil, 'create_db_session', MagicMock(return_value=DbUtil.create_db_session("sqlite:///:memory:")))
    def test_delete_location(self):
        self.db_util.save(self.test_location_obj)
        self.assertTrue(len(self.db_util.find_all())==1)
        self.db_util.delete_location(self.test_location['location_name'])
        self.assertTrue(len(self.db_util.find_all()) == 0)

    @patch.object(DbUtil, 'create_db_session', MagicMock(return_value=DbUtil.create_db_session("sqlite:///:memory:")))
    @patch('app.dbutil.requests.get')
    def test_save_selected_location(self,mock_get):
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = self.test_util.load_json_from_file("test/add_city_autocomplete.json")
        self.assertFalse(self.db_util.location_exists("Glasgow"))
        self.db_util.save_selected_location('Glasgow,United Kingdom')
        self.assertTrue(self.db_util.location_exists("Glasgow"))

    @patch.object(DbUtil, 'create_db_session', MagicMock(return_value=DbUtil.create_db_session("sqlite:///:memory:")))
    def test_save_or_update_settings(self):
        self.db_util.save_or_update_settings("celsius")
        settings = self.db_util.get_default_tem_unit()
        self.assertEqual(str(settings),"celsius")
        self.db_util.save_or_update_settings("fahrenheit")
        new_settings = self.db_util.get_default_tem_unit()
        self.assertEqual(str(new_settings), "fahrenheit")

    @patch.object(DbUtil, 'create_db_session', MagicMock(return_value=DbUtil.create_db_session("sqlite:///:memory:")))
    def test_get_default_tem_unit(self):
        self.db_util.save_or_update_settings("celsius")
        temp_unit = self.db_util.get_default_tem_unit()
        self.assertEqual(str(temp_unit),"celsius")

    @patch.object(DbUtil, 'create_db_session', MagicMock(return_value=DbUtil.create_db_session("sqlite:///:memory:")))
    def test_load_default_settings_if_empty(self):
        self.db_util.load_default_settings_if_empty()
        settings = self.db_util.get_default_tem_unit()
        self.assertEqual(str(settings), "celsius")
