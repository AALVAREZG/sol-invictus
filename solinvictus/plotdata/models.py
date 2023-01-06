from django.db import models
from .constants import UPPER_LAT_LIMIT, LOWER_LAT_LIMIT
from .constants import EAST_LON_LIMIT, WEST_LON_LIMIT

# Create your models here.


class Location(models.Model):
    lat = models.DecimalField(max_digits=8, decimal_places=4)
    lon = models.DecimalField(max_digits=8, decimal_places=4)
    loc_description_text = models.CharField(max_length=200)

    def __str__(self):
        return f'Location: {self.loc_description_text}\n \
                            --> lat: {self.lat}, lon: {self.lon}'

    def is_within_limits(self):
        lat_limit_check = UPPER_LAT_LIMIT >= self.lat >= LOWER_LAT_LIMIT
        lon_limit_check = EAST_LON_LIMIT >= self.lon >= WEST_LON_LIMIT
        print('lat: ', lat_limit_check, ', lon: ', lon_limit_check)
        return (lat_limit_check & lon_limit_check, lat_limit_check, lon_limit_check)


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
