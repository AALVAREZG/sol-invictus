from django.test import TestCase
from .models import Location
from .constants import OUTOFBOUND_MESSAGE, UPPER_LAT_LIMIT, LOWER_LAT_LIMIT
from .constants import EAST_LON_LIMIT, WEST_LON_LIMIT
from django.urls import reverse
import random
import datetime


class LocationBoundsTests(TestCase):

    def test_location_is_within_limits_outbound(self):
        """
        test location is between supported limits
        UPPER_LAT_LIMIT = 63.0
        LOWER_LAT_LIMIT = 34.0
        EAST_LON_LIMIT = 39.0
        WEST_LON_LIMIT = -24.0
        """
        _lat = 71.94
        _lon = -37.79
        outofbound_location = Location(
                            lat=_lat,
                            lon=_lon,
                            loc_description_text="unsupported location")
        result, lat_limit_check,  lon_limit_check = outofbound_location.is_within_limits()                   
        print('outbound lat ', lat_limit_check, 'lon ', lon_limit_check)
        self.assertIs(result, False)
    
    def test_location_is_within_limits_within(self):
        """
        test location is between supported limits
        UPPER_LAT_LIMIT = 63.0
        LOWER_LAT_LIMIT = 34.0
        EAST_LON_LIMIT = 39.0
        WEST_LON_LIMIT = -24.0
        """
        _lat = 41.79
        _lon = -3.79
        within_location = Location(
                            lat=_lat,
                            lon=_lon,
                            loc_description_text="unsupported location")
        result, lat_limit_check,  lon_limit_check = within_location.is_within_limits()                   
        print('within: lat ', lat_limit_check, 'lon ', lon_limit_check)
        self.assertIs(result, True)


    def test_location_is_within_limits_outbound_lat(self):
        """
        test location is between supported limits
        UPPER_LAT_LIMIT = 63.0
        LOWER_LAT_LIMIT = 34.0
        EAST_LON_LIMIT = 39.0
        WEST_LON_LIMIT = -24.0
        """

        _lat_l1 = [random.uniform(UPPER_LAT_LIMIT, 85.0) for i in range(5)]
        _lat_l2 = [random.uniform(-73.0, LOWER_LAT_LIMIT) for i in range(5)]
        _lat_l = _lat_l1 + _lat_l2
        _lon_l = [random.uniform(WEST_LON_LIMIT, EAST_LON_LIMIT) for i in range(10)]
        outofbound_location = Location(
                            lat=random.choice(_lat_l),
                            lon=random.choice(_lon_l),
                            loc_description_text=f"unsupported location created by: {self.__class__}")
        result, lat_limit_check,  lon_limit_check = outofbound_location.is_within_limits()
        print('outbound_lat lat:', lat_limit_check, 'lon ', lon_limit_check)
        self.assertIs(result, False)

    def test_location_is_within_limits_outbound_lon(self):
        """
        test location is between supported limits
        UPPER_LAT_LIMIT = 63.0
        LOWER_LAT_LIMIT = 34.0
        EAST_LON_LIMIT = 39.0
        WEST_LON_LIMIT = -24.0
        """

        _lon_l1 = [random.uniform(-180.0, WEST_LON_LIMIT) for i in range(5)]
        _lon_l2 = [random.uniform(EAST_LON_LIMIT, 180.0) for i in range(5)]
        _lon_l = _lon_l1 + _lon_l2
        _lat_l = [random.uniform(UPPER_LAT_LIMIT, LOWER_LAT_LIMIT) for i in range(10)]
        outofbound_location = Location(
                            lat=random.choice(_lat_l),
                            lon=random.choice(_lon_l),
                            loc_description_text="unsupported location")
        result, lat_limit_check,  lon_limit_check = outofbound_location.is_within_limits()                   
        print('outbound_lon, lat ', lat_limit_check, 'lon ', lon_limit_check)
        self.assertIs(result, False)


class LocationIndexViewTests(TestCase):
    def test_unsupported_location(self):
        """
        Check VIEW error message for a unsupported location
        """
        _lat = 71.94
        _lon = -37.79
        txt = f"unsupported location created by: {self.__class__} at {datetime.datetime.now()}"
        outofbound_location = Location(
                            lat=_lat,
                            lon=_lon,
                            loc_description_text=f"unsupported location created by: {self.__class__}")
        outofbound_location.save()
        response = self.client.get(reverse('plotdata:index'), args=(outofbound_location.pk,))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, OUTOFBOUND_MESSAGE)
        self.assertIsNone(response.context['pvdata'])
